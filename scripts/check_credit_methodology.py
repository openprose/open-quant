"""Check explicit numeric cells and identities, not arbitrary document semantics."""
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT/'examples/credit-methodology'
ORIGINAL = ROOT/'examples/credit-loss-review'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tables(text):
    groups=[]
    for block in re.findall(r'(?:^\|.*\n)+',text,re.M):
        rows=[[c.strip() for c in line.split('|')[1:-1]] for line in block.strip().splitlines()]
        groups.append(rows[2:])
    return groups


def check_cells(packet,document):
    groups=tables(document)
    assert len(groups)==2 and len(groups[0])==4 and len(groups[1])==6
    selected=packet['selected_method']['intervals']
    observed=packet['observed_probabilities']['intervals']
    constructions=packet['observed_constructions']
    assert [row['id'] for row in constructions]==['interval_mass','cumulative_as_interval','conditional_as_unconditional','hazard_times_interval','recovery_as_loss','undiscounted']
    def close(actual,expected,tolerance):
        assert math.isfinite(float(actual)) and abs(float(actual)-expected)<=tolerance,(actual,expected)
    cells=0
    for row,binding,prob,loss in zip(groups[0],selected,observed,constructions[0]['rows']):
        assert row[0]==binding['id']==prob['id']==loss['interval_id']
        assert row[1]==f"({binding['start_years']:g},{binding['end_years']:g}]"
        for col,value,tolerance in [(2,binding['exposure_usd'],1e-7),(3,binding['loss_fraction'],1e-12),(4,prob['unconditional_default'],5e-13),(5,prob['conditional_default'],5e-13),(6,loss['expected_loss_usd'],5e-7)]:
            close(row[col],value,tolerance);cells+=1
        expected=prob['unconditional_default']*binding['exposure_usd']*binding['loss_fraction']*prob['discount_factor']
        close(loss['expected_loss_usd'],expected,1e-7)
    for row,source in zip(groups[1],constructions):
        assert row[0]==source['id']
        close(row[1],source['total_expected_loss_usd'],5e-7)
        close(row[2],source['difference_from_interval_mass_construction_usd'],5e-7)
        cells+=2
    close(sum(x['unconditional_default'] for x in observed),packet['observed_probabilities']['nodes'][-1]['cumulative_default'],1e-12)
    close(sum(x['expected_loss_usd'] for x in constructions[0]['rows']),constructions[0]['total_expected_loss_usd'],1e-7)
    return cells


if __name__=='__main__':
    packet=json.loads((ORIGINAL/'inputs/complete.json').read_text())
    receipt=json.loads((ORIGINAL/'receipt.json').read_text())
    assert digest(ORIGINAL/'inputs/complete.json')==receipt['packets']['complete']['sha256']
    assert digest(ORIGINAL/'model/measure.py')==receipt['source_sha256']
    document=(EXAMPLE/'sample-results/document.md').read_text()
    assert len(document.split()) < 1500
    cells=check_cells(packet,document)
    result=(EXAMPLE/'sample-results/result.md').read_text()
    reviews=(EXAMPLE/'sample-results/reviews.md').read_text()
    for filename,sha in re.findall(r'\| (document.md|reviews.md) \| ([0-9a-f]{64}) \|',result):
        assert digest(EXAMPLE/'sample-results'/filename)==sha
    assert len(re.findall(r'\| (document.md|reviews.md) \|',result))==2
    sources=re.findall(r'`([^`]+)` — SHA-256 `([0-9a-f]{64})`',result)
    assert len(sources)==14 and len({path for path,_ in sources})==14
    for path,sha in sources: assert digest(ROOT/path)==sha,path
    plan=tables(reviews)[0]
    assert [r[0] for r in plan]==[f'D{i}' for i in range(1,9)]
    assert len(tables(reviews)[1])==9 and len(tables(reviews)[2])==9
    assert document.count('[INSTITUTION-SUPPLIED:')==3
    assert 'Mode: `public-methodology`' in document and 'Mode: `public-methodology`' in reviews and 'Mode: `public-methodology`' in result
    rejected=[]
    for name,old,new in [('wrong loss','49381.900706','49382.900706'),('wrong exposure','1000000','1000001'),('wrong conditional denominator','0.213372138933','0.148864689977'),('wrong construction total','282281.768182','133399.097125'),('erased difference','148882.671057','0.000000'),('wrong interval endpoint','(3,5]','(3,4]'),('wrong row identity','| I2 |','| I1 |'),('probability as percent','0.100292575651','10.0292575651')]:
        assert old in document
        try: check_cells(packet,document.replace(old,new,1))
        except (AssertionError,ValueError,KeyError,TypeError):rejected.append(name)
        else:raise AssertionError('Undetected mutation: '+name)
    print(json.dumps({'numeric_cells_checked':cells,'document_words':len(document.split()),'requirement_map_rows':len(plan),'choice_rows':9,'citation_groups':9,'selected_identities':len(sources),'rejected_mutations':rejected,'scope':'Authored reference cells, structure and identities only. No numerical model execution, arbitrary prose assessment or agent qualification.'},indent=2))

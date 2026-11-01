from domain import evaluate


def test_three_complete_bags_and_preview():
    assert evaluate("""const e=createEngine(()=>0.37);e.start('g');const kinds=[];let preview=true;for(let i=0;i<21;i++){kinds.push(e.view().active.kind);const next=e.view().queue[0];e.fixture({board:emptyBoard()});for(let j=0;j<22;j++)e.act('softDrop');e.advance(1000);preview&&=e.view().active.kind===next;}console.log(JSON.stringify([Array.from({length:3},(_,i)=>[...new Set(kinds.slice(i*7,i*7+7))].sort().join('')),preview]));""", fixture=True) == [['IJLOSTZ']*3, True]

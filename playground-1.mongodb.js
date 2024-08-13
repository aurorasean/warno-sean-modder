
use('sean-modder');

// db['decks'].find({ 'namespace': { "$regex": '(10Pt)' } }).limit(10).toArray();

db['modded-decks'].find({}).toArray();
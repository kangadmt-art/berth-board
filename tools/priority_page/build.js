// build.js <prio.json> <out.html> — puts the extracted data into the page template
const fs=require('fs');const t=fs.readFileSync(__dirname+'/template.html','utf8');const d=fs.readFileSync(process.argv[2],'utf8');
if(!t.includes('/*DATA*/null'))throw new Error('placeholder missing');fs.writeFileSync(process.argv[3],t.replace('/*DATA*/null',()=>d.replace(/</g,'\\u003c')));console.log('built',process.argv[3]);

import fs from 'node:fs';
import crypto from 'node:crypto';
import {createInMemoryRagClient} from './rag-client.ts';
const rows=fs.readFileSync(new URL('./corpus.jsonl',import.meta.url),'utf8').trim().split('\n').map(JSON.parse);
const client=createInMemoryRagClient({jsonlPath:new URL('./corpus.jsonl',import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1')});
await client.warmup();
const cases=[
 {name:'중3 · 이차방정식 · 쉬움',keyword:'방정식',query:{school_level:'middle',grade:3,topic_code:'9수02-09',problem_type:'short_answer',difficulty:'easy',k:8}},
 {name:'중1 · 일차방정식 · 쉬움',keyword:'방정식',query:{school_level:'middle',grade:1,topic_code:'9수02-03',problem_type:'short_answer',difficulty:'easy',k:8}},
 {name:'중3 · 이차방정식 · 어려움 (해당 문항 없음)',keyword:'방정식',query:{school_level:'middle',grade:3,topic_code:'9수02-09',problem_type:'short_answer',difficulty:'hard',k:8}}
];
const brief=p=>({id:p.id.problem_id,grade:p.curriculum.grade,topic:p.curriculum.topic_name,topic_code:p.curriculum.topic_code,difficulty:p.problem.difficulty,question:p.problem.question_text});
const matches=(p,q)=>p.curriculum.school_level===q.school_level && p.curriculum.grade===q.grade && p.curriculum.topic_code===q.topic_code && p.problem.problem_type===q.problem_type && p.problem.difficulty===q.difficulty;
const output=[];
for(const c of cases){
 const baseline=rows.filter(p=>[p.curriculum.topic_name,p.problem.question_text,p.problem.explanation_text].join(' ').includes(c.keyword)).sort((a,b)=>a.id.problem_id.localeCompare(b.id.problem_id));
 const actual=await client.search(c.query);
 output.push({...c,baseline:baseline.map(brief),baseline_matching:baseline.filter(p=>matches(p,c.query)).length,structured:actual.map(r=>({...brief(rows.find(p=>p.id.problem_id===r.item_id)),score:r.similarity})),structured_matching:actual.filter(r=>matches(rows.find(p=>p.id.problem_id===r.item_id),c.query)).length});
}
const hash=f=>crypto.createHash('sha256').update(fs.readFileSync(new URL(f,import.meta.url))).digest('hex');
const result={executed_at:new Date().toISOString(),node:process.version,code_commit:'3eb62c8f5b60bb19795fb93034d15b3875d60c6f',corpus_commit:'62f2a41edcba83a9f53ec6add56697ca9911ab3a',code_sha256:hash('./rag-client.ts'),corpus_sha256:hash('./corpus.jsonl'),corpus_size:rows.length,method:'baseline: 단원·문제·해설에서 키워드 포함 여부, ID 정렬. structured: 원본 PR #8 RagClient 실행. 두 방식 모두 k=8 범위 내 모든 결과 표시.',limitation:'공개 seed 7건에 대한 조건 필터 동작 비교입니다. AI Hub 전체 데이터나 의미 검색 정확도, 임베딩 검색 우수성을 평가하지 않습니다. 질의는 필터 동작을 확인하기 위해 선정했습니다.',cases:output};
fs.writeFileSync(process.argv[2] ?? new URL('./result.json',import.meta.url),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));

import json
from pathlib import Path
from rag.retriever_tool import retrieve_context
eval_path = Path(__file__).parent.parent / "eval/test_set.jsonl"
print("Eval path:", eval_path)

def main():
    path = eval_path
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    print(f"Loaded {len(rows)} eval queries.")
    print('rows:', rows)

    hit = 0
    total = len(rows)

    for r in rows:
        q = r["q"]
        gold = r["gold_source"]
        res = retrieve_context(q)
        print("retrieve_context:", res)
        sources = [Path(m["source"]).name for m in res.get("matches", [])]
        # print("sources:", sources)
        

        ok = gold in sources
        hit += 1 if ok else 0
        print('ok:', ok)
        print('hit:', hit)

        print("Q:", q)
        print("Top sources:", sources)
        print("Expected:", gold, "| HIT" if ok else "| MISS")
        
        print("-" * 60)
        

    print(f"Hit@K: {hit}/{total} = {hit/total:.2%}")


if __name__ == "__main__":
    main()

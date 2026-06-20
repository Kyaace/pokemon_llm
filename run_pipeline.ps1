python -u code/corpus_generation/expert_system.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -u code/corpus_generation/generate_anime_corpus.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -u code/corpus_generation/generate_qa_corpus.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -u code/corpus_generation/tokenize_corpus.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -u code/corpus_generation/verify_corpus_vocab.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

echo "ALL DONE!"

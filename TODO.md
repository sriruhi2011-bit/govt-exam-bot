# TODO — govt-exam-bot (Scoped: items 1-4)

## Step 1: Add AI response caching (reduce duplicate AI calls)
- [x] Update `ai_engine.py` with in-memory cache keyed by provider + prompt hash + params
- [x] Expose `query_cached()` helper
- [x] Wire `query_cached()` into:
  - [x] `NewsFilter.ai_analyze()`
  - [x] `ContentGenerator.create_summary()`
  - [x] `QuizGenerator.make_questions()`

## Step 2: Enforce per-category limits + reduce AI calls in filtering/news selection
- [x] Add per-category quota constant(s) in `config/settings.py`
- [x] Update `news_filter.py` to stop scanning/AI-evaluating once quotas per category are satisfied

## Step 3: Consistent per-category posting limits
- [x] Update `content_generator.py` to use configured per-category limit (remove hardcoded `[:4]`)
- [x] Ensure header counts match actual included articles

## Step 4: Improve quiz correctness + per-category selection + reduce AI calls
- [x] Update `quiz_generator.py`:
  - [x] Select quiz articles using per-category quotas (instead of first 15)
  - [x] Validate and normalize `correct_answer` to `A|B|C|D`
  - [x] Regenerate quiz for an article when parsed data is malformed (bounded retries)
- [x] Ensure generated Telegram quiz polls have correct option id

## Step 5: Scheduling robustness
- [x] Update `main.py` to call `check_missed_jobs()` periodically during runtime (e.g., every 60s)

## Step 6: Smoke tests
- [ ] `python main.py test`
- [ ] `python main.py news`
- [ ] `python main.py quiz`

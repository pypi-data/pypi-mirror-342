# tests/test_metrics.py
from doc_quality.metrics import get_metrics

def test_word_count():
    sample = "### Bug Fixes\
* **async component:** memory leak after synchronous async loading (#9275) d21e931, closes #9275 #9229\
* **core:** dedupe lifecycle hooks during options merge 0d2e9c4, closes #9199\
* **core:** fix merged twice bug when passing extended constructor to mixins (#9199) 743edac, closes #9199 #9198\
* **ssr:** support rendering comment (#9128) b06c784, closes #9128\
### Notable Changes\
- `Vue.config.performance` now defaults to `false` due to its impact on dev mode performance. Only turn it on when you need it.\
### Improvements\
- Now warns usage of camelCase props when using in-DOM templates. (@CodinCat via #5161)\
- Now warns when template contains text outside of root element. (@xujiongbo via #5164)\
"
    metrics = get_metrics(sample)
    assert metrics["M1_Words"] >= 10

# Install deps

    python -m pip install nltk
    wget https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-MacOSX-3.2.3.tar.gz https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz
    mkdir -p treetagger && tar -xzf tree-tagger-MacOSX-3.2.3.tar.gz --directory treetagger && tar -xzf tagger-scripts.tar.gz --directory treetagger
    wget https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/russian.par.gz
    gunzip -c russian.par.gz > treetagger/lib/russian.par

# Run

    python mixer.py < test_en.txt 2>/dev/null
    python mixer.py --tagger treetagger < test_ru.txt 2>/dev/null

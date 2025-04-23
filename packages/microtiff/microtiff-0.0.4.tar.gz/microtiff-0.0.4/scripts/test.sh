#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR/..
echo "About to run tests on IFCB & LISST-Holo2 data"
echo "NOTE: Test data is not included in the microtiff git repository due to licensing concerns. Information on where to obtain this data is listed in the TESTING.md file."
rm testdata/ifcb-1/*.json 2> /dev/null
rm testdata/ifcb-1/*.tiff 2> /dev/null
python3 src/microtiff/ifcb.py testdata/ifcb-1/*.roi
SHAOUT=($(sha256sum -b testdata/ifcb-1/*.tiff testdata/ifcb-1/*.json | sha256sum))
if [ "${SHAOUT[0]}" = "3bf9cf416d7008714d111d3995cf039bdec4d1b3fb01e1bb69ba72f961db7b7d" ]; then
    echo "[PASS] IFCB Test 1"
    rm testdata/ifcb-1/*.json
    rm testdata/ifcb-1/*.tiff
else
    echo "[FAIL] IFCB Test 1 - Hash (${SHAOUT[0]}) did not match expected output"
fi
rm testdata/ifcb-2/*.json 2> /dev/null
rm testdata/ifcb-2/*.tiff 2> /dev/null
python3 src/microtiff/ifcb.py testdata/ifcb-2/*.roi
SHAOUT=($(sha256sum -b testdata/ifcb-2/*.tiff testdata/ifcb-2/*.json | sha256sum))
if [ "${SHAOUT[0]}" = "362edc58a2e1e1ea34500fb74ff290297068bb5bff8d0594c1546eea6fa10a81" ]; then
    echo "[PASS] IFCB Test 2"
    rm testdata/ifcb-2/*.json
    rm testdata/ifcb-2/*.tiff
else
    echo "[FAIL] IFCB Test 2 - Hash (${SHAOUT[0]}) did not match expected output"
fi
rm testdata/lisst-holo-1/*.json 2> /dev/null
rm testdata/lisst-holo-1/*.tiff 2> /dev/null
python3 src/microtiff/lisst_holo.py testdata/lisst-holo-1/*.pgm
SHAOUT=($(sha256sum -b testdata/lisst-holo-1/*.tiff testdata/lisst-holo-1/*.json | sha256sum))
if [ "${SHAOUT[0]}" = "79b9e43c83b155c63e804002953fef5d1c871f757d6a29206f144b93a506b1b3" ]; then
    echo "[PASS] LISST-Holo Test 1"
    rm testdata/lisst-holo-1/*.json
    rm testdata/lisst-holo-1/*.tiff
else
    echo "[FAIL] LISST-Holo Test 1 - Hash (${SHAOUT[0]}) did not match expected output"
fi

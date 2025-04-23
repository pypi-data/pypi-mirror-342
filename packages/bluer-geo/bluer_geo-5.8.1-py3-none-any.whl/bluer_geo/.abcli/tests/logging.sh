#! /usr/bin/env bash

function test_bluer_geo_logging() {
    local options=$1

    bluer_geo log \
        filename=1050010040277300-visual.tif,$options \
        $BLUE_GEO_TEST_DATACUBE_MAXAR_OPEN_DATA
}

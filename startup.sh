#!/usr/bin/env bash

flask db upgrade
flask cmd update_segments

#!/usr/bin/env bash

flask db upgrade
flask cmd load_segments
flask cmd latest_entry

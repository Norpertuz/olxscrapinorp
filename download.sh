#!/bin/bash

# --- Komputery stacjonarne ---
for page in {1..25}; do
    file="files/olx_page_pc_${page}.html"
    echo "Pobieram stronę PC $page → $file"

    wget -O "$file" \
    --header="User-Agent: Mozilla/5.0" \
    "https://www.olx.pl/elektronika/komputery/komputery-stacjonarne/?search%5Border%5D=relevance:desc&search%5Bfilter_float_price:from%5D=30&search%5Bfilter_float_price:to%5D=400&view=grid&page=$page"
done

# --- Karty graficzne ---
for page in {1..25}; do
    file="files/olx_page_gpu_${page}.html"
    echo "Pobieram stronę GPU $page → $file"

    wget -O "$file" \
    --header="User-Agent: Mozilla/5.0" \
    "https://www.olx.pl/elektronika/komputery/podzespoly-i-czesci/karty-graficzne/?search%5Bfilter_float_price:from%5D=10&search%5Bfilter_float_price:to%5D=150&view=grid&page=$page"
done

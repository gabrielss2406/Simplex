latest_file=""

for file in in/*
do
    filename="$(cut -d'/' -f2 <<<"$file")"
    python src/main.py "$file" > out/"$filename" 2>&1
    latest_file="out/$filename"
done

# Abre o último arquivo gerado
if [ -n "$latest_file" ]; then
    # Verifica o sistema operacional
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$latest_file"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        start "$latest_file"
    else
        echo "Sistema operacional não suportado para abrir automaticamente o arquivo."
    fi
fi

# Examination 
Inlämning är för Anna Wester. 

## Se fil i root mappen Anna_Wester_1.txt
Filen ger en beskrivning av inlämningsuppgiften och vilka punkter som ingår i projektet.

## Delad mapp för Github
https://github.com/AnnaWester73/anna_wester_fruitloop

## Starta projektet
För att starta spelet.
Jag har gjort enligt tips att gå in i Edit configuration och adderat src-game för att starta spelet.
python -m src.game är skapad i "Run configuration"

## Testfall TDD gäller för player.py och pickups.py och ligger i en undermapp /tests
I rooten i projektet skriv i terminal skriv
python -m src.game
Totalt 14 testfall skapade


```commandline
python -m src.game
```

Tips! Du kan spara denna rad som en "run configuration" i PyCharm.
1. Välj "Edit configurations..."
2. Ändra i sektionen "run" så det står `module` i stället för `script`
3. Skriv `src.game` i rutan till höger om `module`


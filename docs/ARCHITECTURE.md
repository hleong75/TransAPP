# Architecture TransAPP

## Objectif

TransAPP fournit une base open-source pour une application de navigation multimodale offline inspirée de Transito. Le noyau est écrit en Python modulaire pour un futur portage Android.

## Modules principaux

- `transapp.config` : configuration centralisée (paths, URLs de download).
- `transapp.engine.osm` : téléchargement et représentation minimale OSM vectorielle.
- `transapp.engine.gtfs` : ingestion GTFS automatique depuis transport.data.gouv.fr.
- `transapp.engine.router` : routage multimodal rapide offline.
- `transapp.evaluation` : auto-évaluation performance, couverture, stabilité.
- `transapp.agents.*` : agents IA (architecte, builder, reviewer, validator, optimizer) coordonnés par un maître.

## Flux automatique

1. `bootstrap` télécharge ou recharge les datasets.
2. `RoutePlanner` calcule l’itinéraire multimodal le plus rapide.
3. `Evaluator` mesure la couverture et la stabilité.
4. `MasterAgent` déclenche les propositions d’amélioration.

## Pipeline GitHub

Le pipeline GitHub Actions exécute les tests unitaires et prépare le terrain pour des PR internes générées par les agents.

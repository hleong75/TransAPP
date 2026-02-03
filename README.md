# TransAPP

Base open-source pour une application Android de navigation multimodale offline.

## Android (squelette)

Le module `android-app/` fournit une application Android minimale qui affiche une vue d'accueil. La logique offline reste dans le package Python en attendant l'intégration native.

### Compiler localement (nécessite Android SDK)

```bash
./gradlew :android-app:assembleDebug
```

## Démarrage rapide (Python)

```bash
python -m transapp.cli
```

## Architecture

Consultez [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

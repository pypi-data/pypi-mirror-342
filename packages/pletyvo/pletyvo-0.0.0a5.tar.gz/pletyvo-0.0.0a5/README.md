> [!WARNING] 
> This is an unstable version. Changes may be backwards incompatible

# `py-pletyvo`

Implementation of the client and protocols of [the Pletyvo decentralized platform](https://pletyvo.osyah.com/) in Python.

Чому це важливо? [Плетиво: децентралізовані застосунки](https://osyah.com/stattya/pletyvo-detsentralizovani-zastosunky/)

## Install

```bash
pip install -U pletyvo
```

## Usage

```py
from pletyvo.client import http
from pletyvo.protocol import dapp, delivery


signer: dapp.abc.Signer = dapp.ED25519.gen()

# Двигун який буде використовуватися для запитів.
# 
engine: http.abc.HTTPClient = http.HTTPDefault(
    config=http.Config(
        url="http://testnet.pletyvo.osyah.com",
    ),
)


service = http.HTTPService._(
    engine=engine,
    signer=signer,
)

async def main() -> None:
    for event in await service.dapp.events.get():
        print(event.body.data)
```

Перш ніж користувач зможе взаємодіяти з децентралізованими застосунками, йому необхідно згенерувати пару криптографічних ключів, які надалі будуть використовуватися для підпису його вхідних даних.

```py
from pletyvo.protocol import dapp

signer: dapp.abc.Signer = dapp.ED25519.gen()
```

Пара криптографічних ключів можуть генеруватися багатьма способами, але оптимальний для більшості — це використання мнемонічної фрази. В такому разі користувачу доведеться зберігати мнемонічну фразу в таємниці, оскільки її розкриття іншим несе під собою надання доступу до його облікового запису, що ймовірно призведе до неприємних наслідків.

![](docs/service-graph.svg)

Варто зазначити, що використання криптографії є цілком безпечним методом, тому що тільки користувач володіє доступом до власних даних, а будь-яка їх компрометація є безглуздою, оскільки кожний може перевірити автентичність завдяки підпису.

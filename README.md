#  Sopra Steria Habnds on Bedrock-lab 

<img width="1181" alt="image" src="img/header.png">


## Hvordan jobbe med oppgaven

1. Lag en fork til din egen GitHub-bruker av dette repositoryet 
2. Start et GitHub Codespace (trykk .)

## Litt om AWS Bedrock 

AWS Bedrock er en tjeneste fra Amazon som gir tilgang til ulike KI-modeller uten behov for å håndtere den tekniske infrastrukturen selv. I denne oppgaven skal du bli kjent med Amazons egen generative KI-modell for bilder, "Titan."

Ved å bruke denne modellen kan du sende inn et "prompt," som for eksempel "en solnedgang over fjorden med palmer, fjell, og en elg i bakgrunnen." Bedrock vil deretter generere et bilde som samsvarer med beskrivelsen.

Funksjonaliteten vi trenger fra AWS Bedrock er foreløpig ikke tilgjengelig i Irland, så du vil se referanser til regionen "us-east-1" i koden. Likevel skal du bruke Irland (eu-west-1) som region for infrastrukturen din. Det er ingen problem for en Lambda-funksjon i Irland å benytte Bedrock-tjenesten i USA.

#  Oppgave: Implementer en Lambda-funksjon med SAM

I dette repositoryet finner du tre python-programmer. Programmene har "noen" utfordringer med tanke på kodekvalitet, men har fungerende kode for å genere vide, bilde og tekst.

1. generate_image.py - Lager et bilde basert på et tekst-prompt
2. generate_video.py - Lager en video basert på et tekst-prompt
3. generate_exam_question lager et tilfeldig eksamenssprørsmål til AWS Certified Developer Associate sertifiseringen

I klassens delte AWS-konto finnes det en S3-bucket med navnet `sopra-steria-ai-day-25`. Din oppgave er å ta utgangspunkt en eller flere av Python-programmene og implementere funksjonaliteten som en AWS Lambda-funksjon ved hjelp av AWS SAM (Serverless Application Model). 

Prøv gjerne pythonkoden først for å bli kjent med tjenesten. I ditt codespace kan du lage et nytt Python `virtual environment`

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install boto3

python generate_image.py
python generate_video.py
generate_exam_question.py

```

Et virtual environment i Python er et isolert miljø der du kan installere pakker og avhengigheter uten å påvirke resten av systemet. Det gjør det mulig å ha forskjellige prosjekter med ulike pakkeversjoner på samme maskin.

Eksempelbilde

<img width="1014" alt="image" src="img/croissant.png">

#### Trinn 1: Opprett en SAM-applikasjon

Sett opp infrastrukturen for Lambda-funksjonen - Bruk `sam init` til å generere en ny SAM-applikasjon.

#### Trinn 2: Skriv Lambda-funksjonen

Flytt koden fra Python-programmet og skriv det om til en Lambda-funksjon. Funksjonen skal motta en forespørsel via HTTP.


####  Test og deploy SAM-applikasjonen

1. Bygg Lambda-funksjonen lokalt med SAM CLI for å sikre at den fungerer som forventet.
2. Deploy applikasjonen. Etter deploy bør du verifisere at POST-endepunktet fungerer, og at Lambda-funksjonen kan lagre filer i S3-bucketen `sopra-steria-ai-day-25`.

#### Tips og  anbefalinger
- **Timeout**: Husk at Lambdafunksjoner har en konfigurerbar timeout, viktig spesielt for cideo
- **IAM-rolle**: Sørg for at Lambda-funksjonen har nødvendige tillatelser til å skrive til S3-bucketen, og kalle tjenesten AWS Bedrock
- **Regionkonfigurasjon**: Husk at regionen for infrastrukturen skal være `eu-west-1`, selv om ressurser som AWS Bedrock kan ligge i andre regioner.

## Bonusoppgaver (velg minst én)

For å utfordre deg selv litt ekstra kan du velge en eller flere av følgende bonusoppgaver. Disse bygger videre på Lambda-funksjonen du allerede har laget:

### 1. **Frontend-integrasjon**

Lag en enkel frontend (HTML/JavaScript eller React) som lar en bruker skrive inn en prompt i et tekstfelt og deretter kaller ditt API Gateway-endepunkt. Resultatet skal være at bildet lastes inn og vises direkte i nettleseren.

*Hint:* Du kan bruke `fetch` i JavaScript for å gjøre POST-kallet til API Gateway, og hente ut S3-URL-en fra responsen.

### 2. **Metadata i DynamoDB**

Utvid løsningen slik at hvert genererte bilde også registreres i en DynamoDB-tabell. Tabellen kan f.eks. lagre:

* kandidatnummer / brukernavn
* prompt (teksten brukt for å lage bildet)
* tidspunkt for generering
* S3-path til bildet

*Hint:* Bruk `boto3` sitt DynamoDB-API (`put_item`). Husk IAM-tilgang.

### 3. **Egen bucket og IAM-policy**

I stedet for å bruke den delte S3-bucketen, opprett din egen bucket i AWS-kontoen.

* Lag en bucket policy som tillater at API Gateway/Lambda kan skrive bilder.
* Sett opp en CloudFront-distribusjon foran bucketen, slik at bildene kan aksesseres via en offentlig URL med lavere latency.

 *Hint:* Husk at du kan sette opp bucket policy direkte i SAM-templatefilen.

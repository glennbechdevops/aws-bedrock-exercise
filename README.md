#  Sopra Steria Habnds on Bedrock-lab 

<img width="1181" alt="image" src="img/header.png">


## Hvordan jobbe med oppgaven

1. Lag en fork til din egen GitHub-bruker av dette repositoryet 
2. Start et GitHub Codespace (trykk .)

## Litt om AWS Bedrock 

AWS Bedrock er en tjeneste fra Amazon som gir tilgang til ulike KI-modeller uten behov for å håndtere den tekniske infrastrukturen selv. I denne oppgaven skal du bli kjent med Amazons egen generative KI-modell for bilder, "Titan."

Ved å bruke denne modellen kan du sende inn et "prompt," som for eksempel "en solnedgang over fjorden med palmer, fjell, og en elg i bakgrunnen." Bedrock vil deretter generere et bilde som samsvarer med beskrivelsen.

Funksjonaliteten vi trenger fra AWS Bedrock er foreløpig ikke tilgjengelig i Irland, så du vil se referanser til regionen "us-east-1" i koden. Likevel skal du bruke Irland (eu-west-1) som region for infrastrukturen din. Det er ingen problem for en Lambda-funksjon i Irland å benytte Bedrock-tjenesten i USA.

## Lag AWS Credentials 

* Følg veiledningen her for å lage Access Key og Secret Access Key  - https://github.com/glennbechdevops/aws-iam-accesskeys
* Sett verdiene som CodeSpaces/Repository secrets

<img width="2652" height="1186" alt="image" src="https://github.com/user-attachments/assets/e5eb3cc1-8310-4515-b0f8-54acbd6b2db9" />

## Installer nødvendig programvare i ditt CodeSpaces miljø 

* Fra din fork av dette repositoryet, starter du CodeSpaces. Keyboard shortcut er "." 
* Åpne et terminalvindu, 

### Installer AWS CLI 

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Test at CLI og Akesessnøkler er riktig satt opp ved å kjøre 

```
aws s3 ls
```

### Installer SAM

```
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
````

#  Oppgave: Implementer en Lambda-funksjon med SAM

I dette repositoryet finner du tre python-programmer. Programmene har "noen" utfordringer med tanke på kodekvalitet, men har fungerende kode for å genere vide, bilde og tekst.

1. generate_image.py - Lager et bilde basert på et tekst-prompt
2. generate_video.py - Lager en video basert på et tekst-prompt
3. generate_exam_question lager et tilfeldig eksamenssprørsmål til AWS Certified Developer Associate sertifiseringen

Din oppgave er å ta utgangspunkt en eller flere av Python-programmene og implementere de som  AWS Lambda-funksjoner ved hjelp av AWS SAM (Serverless Application Model). 

Prøv gjerne pythonkoden først for å bli kjent med tjenesten. I ditt codespace kan du lage et nytt Python `virtual environment`

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install boto3

python generate_image.py
python generate_video.py
generate_exam_question.py

```

I klassens delte AWS-konto finnes det en S3-bucket med navnet `sopra-steria-ai-day-25` dere kan bruke for lagring av bilder og video


Et virtual environment i Python er et isolert miljø der du kan installere pakker og avhengigheter uten å påvirke resten av systemet. Det gjør det mulig å ha forskjellige prosjekter med ulike pakkeversjoner på samme maskin.

Eksempelbilde

<img width="1014" alt="image" src="img/croissant.png">

#### Trinn 1: Opprett en SAM-applikasjon

Sett opp infrastrukturen for Lambda-funksjonen - Bruk `sam init` til å generere en ny SAM-applikasjon.

#### Trinn 2: Skriv  Lambda-funksjonen og forbedre koden

Flytt koden fra Python-programmet og skriv det om til en Lambda-funksjon. Fokuser først på å få ting til å fungere. Deretter kan du forsøke å forbedre koden ved feks å ikke hardkode bucketnavn og andre verdier - 
men istedet bruke for eksempel environment variabler 

```
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: app.lambda_handler
      Runtime: python3.12
      Environment:
        Variables:
          BUCKET_NAME: my-demo-bucket
```

I Python-koden kan disse leses  med kode som `bucket_name = os.environ.get("BUCKET_NAME", "")`

####  Test og deploy SAM-applikasjonen

1. Bygg Lambda-funksjonen lokalt med SAM CLI for å sikre at den fungerer som forventet.

```
sam build --use-container
```
2. Deploy applikasjonen.

Deploy applikasjonen med 

```
sam deploy .... 
```
Du må selv finne ut av argumentene for `sam deploy`

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

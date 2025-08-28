#  Sopra Steria Hands-on Bedrock-lab 

<img width="1181" alt="image" src="img/header.png">

## Lag en fork

Du må start med å lage en fork av dette repoet til din egen GitHub konto.

<img width="2938" height="1334" alt="image" src="https://github.com/user-attachments/assets/81319cee-9cc0-4658-8de1-f9adb328ac30" />


## Lag AWS Credentials 

* Følg veiledningen her for å lage Access Key og Secret Access Key  - https://github.com/glennbechdevops/aws-iam-accesskeys

## Sett Access Key & secret  som CodeSpaces/Repository secrets

<img width="2652" height="1186" alt="image" src="https://github.com/user-attachments/assets/e5eb3cc1-8310-4515-b0f8-54acbd6b2db9" />

* I din fork, velg "settings" og "Secrets and Variables"
* Velg "Code Spaces" og "New repository secret"
* Legg inn verdier for både AWS_ACCESS_KEY_ID og AWS_SECRET_ACCESS_KEY

## Start et Codespace & Installer nødvendig programvare 

* Fra din fork av dette repositoryet, starter du CodeSpaces. Keyboard shortcut er "."
* Alternativt, velg den grønne "Code", "Velg Codespaces" og "Create codespace from main"
* Fra ditt mnye CodeSpace - Åpne et **terminalvindu**, og velg "Continue working in GitHub Codespaces"
  
### Installer AWS CLI 

I terminalen kjør følgende kommandoer

```
cd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Test at CLI og Akesessnøkler er riktig satt opp ved å kjøre 

```
aws s3 ls
````

## Litt om AWS Bedrock 

AWS Bedrock er en tjeneste fra Amazon som gir tilgang til ulike KI-modeller uten behov for å håndtere den tekniske infrastrukturen selv. I denne oppgaven skal du bli kjent med Amazons egen generative KI-modell for bilder, "Titan."

Ved å bruke denne modellen kan du sende inn et "prompt," som for eksempel "en solnedgang over fjorden med palmer, fjell, og en elg i bakgrunnen." Bedrock vil deretter generere et bilde som samsvarer med beskrivelsen.

Funksjonaliteten vi trenger fra AWS Bedrock er foreløpig ikke tilgjengelig i Irland, så du vil se referanser til regionen "us-east-1" i koden. Likevel skal du bruke Irland (eu-west-1) som region for infrastrukturen din. Det er ingen problem for en Lambda-funksjon i Irland å benytte Bedrock-tjenesten i USA.

### Installer SAM

```
cd /tmp
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

I klassens delte AWS-konto finnes det en S3-bucket med navnet `sopra-steria-ai-day-25` Python koden bruker denne for å lagre bilder- og video, dere kan fortsette med det når dere lager Lambda-funksjoner


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


### Gi Lambdafunksjonen nødvendige rettigheter / IAM Policyer for å bruke bedrock 

Lambdafunskonen trenger rettigheter ti å bruke AWS Bedrock. Endre template.yml, legg til nødvendige rettigheter.

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
- **Timeout**: Husk at Lambdafunksjoner har en konfigurerbar timeout, viktig spesielt for video
- **IAM-rolle**: Sørg for at Lambda-funksjonen har nødvendige tillatelser til å skrive til S3-bucketen, og kalle tjenesten AWS Bedrock
- **Regionkonfigurasjon**: Husk at regionen for infrastrukturen skal være `eu-west-1`, selv om ressurser som AWS Bedrock kan ligge i andre regioner.

## Bonusoppgaver (velg minst én)

For å utfordre deg selv litt ekstra kan du velge en eller flere av følgende bonusoppgaver. Disse bygger videre på Lambda-funksjonen du allerede har laget:

### 1. **Frontend-integrasjon**

Lag en enkel frontend (HTML/JavaScript eller React) som lar en bruker skrive inn en prompt i et tekstfelt og deretter kaller ditt API Gateway-endepunkt. Resultatet skal være at bildet lastes inn og vises direkte i nettleseren.

*Hint:* Du kan bruke `fetch` i JavaScript for å gjøre POST-kallet til API Gateway, og hente ut S3-URL-en fra responsen.

### 2. **Sentimentanalyse for tekstgenerering**

Det kan være greit at for eksempel eksamens-spørsmål-generatoren selv-modererer seg selv og gjør en analyse for potensielt støtende tekst (toxicity)
før teksten skrives ut. Modifiser koden til å gjøre først spørsmåls-generering, og deretter tekstanalyse med comprehend.

### 3. **Metadata i DynamoDB**

Utvid løsningen slik at hvert genererte bilde også registreres i en DynamoDB-tabell. Tabellen kan f.eks. lagre:

* kandidatnummer / brukernavn
* prompt (teksten brukt for å lage bildet)
* tidspunkt for generering
* S3-path til bildet

*Hint:* Bruk `boto3` sitt DynamoDB-API (`put_item`). Husk IAM-tilgang.

### 4. **Egen bucket og IAM-policy**

I stedet for å bruke den delte S3-bucketen, opprett din egen bucket i AWS-kontoen.

* Lag en bucket policy som tillater at API Gateway/Lambda kan skrive bilder.
* Sett opp en CloudFront-distribusjon foran bucketen, slik at bildene kan aksesseres via en offentlig URL med lavere latency.

 *Hint:* Husk at du kan sette opp bucket policy direkte i SAM-templatefilen.

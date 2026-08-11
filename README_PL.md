# System analizy sprawozdań finansowych

## Aplikacja webowa stworzona w Django do zarządzania przedsiębiorstwami oraz analizy sprawozdań finansowych XML (PRS/KRS)

---

## O projekcie

System analizy sprawozdań finansowych jest aplikacją webową napisaną w języku Python z wykorzystaniem frameworka Django.

Projekt powstał jako aplikacja portfolio i został zaprojektowany z myślą o praktycznym zastosowaniu w analizie przedsiębiorstw oraz zarządzaniu danymi finansowymi.

Głównym zadaniem aplikacji jest umożliwienie użytkownikowi zarządzania bazą przedsiębiorstw, importowania sprawozdań finansowych z plików XML pochodzących z systemu PRS/KRS oraz prezentowania najważniejszych informacji finansowych w uporządkowany sposób.

Podczas realizacji projektu wykorzystano technologie stosowane we współczesnych aplikacjach backendowych, takie jak Django, Django REST Framework, PostgreSQL, JWT, Celery, Redis, Docker, pytest oraz wdrożenie produkcyjne na platformie Railway.

Projekt został zaprojektowany jako fundament do dalszego rozwoju. W kolejnych etapach planowane jest rozszerzenie go o bardziej zaawansowaną analizę finansową, wskaźniki ekonomiczne, moduły wspierające ocenę przedsiębiorstw oraz rozwiązania z zakresu Data Science, DevOps i CyberSecurity.

---

# Spis treści

- [Dlaczego powstał ten projekt?](#dlaczego-powstał-ten-projekt)
- [Cele projektu](#cele-projektu)
- [Najważniejsze funkcjonalności](#najważniejsze-funkcjonalności)
- [Architektura aplikacji](#architektura-aplikacji)
- [Model danych](#model-danych)
- [Import sprawozdań finansowych XML](#import-sprawozdań-finansowych-xml)
- [Bezpieczeństwo i izolacja danych użytkowników](#bezpieczeństwo-i-izolacja-danych-użytkowników)
- [REST API](#rest-api)
- [Testy automatyczne](#testy-automatyczne)
- [Deployment](#deployment)
- [Docker](#docker)
- [Celery i zadania asynchroniczne](#celery-i-zadania-asynchroniczne)
- [Responsywność aplikacji](#responsywność-aplikacji)
- [Historia rozwoju projektu](#historia-rozwoju-projektu)
- [Technologie](#technologie)
- [Struktura projektu](#struktura-projektu)
- [Instalacja i uruchomienie projektu](#instalacja-i-uruchomienie-projektu)
- [Panel administratora Django](#panel-administratora-django)
- [Konfiguracja i zmienne środowiskowe](#konfiguracja-i-zmienne-środowiskowe)
- [Dalszy rozwój projektu](#dalszy-rozwój-projektu)
- [Autor](#autor)
- [Licencja](#licencja)

---

# Dlaczego powstał ten projekt?

Większość projektów portfolio prezentuje przede wszystkim gotowy efekt końcowy. Celem tego projektu było jednak nie tylko stworzenie aplikacji internetowej, ale również praktyczne zdobywanie doświadczenia z technologiami wykorzystywanymi przez współczesnych Python Developerów.

Projekt rozwijał się etapami. Każda nowa funkcjonalność była implementowana po opanowaniu kolejnych zagadnień podczas kursu Python Developer. Dzięki temu aplikacja stała się nie tylko projektem portfolio, ale również praktycznym środowiskiem nauki projektowania, implementacji, testowania i wdrażania aplikacji webowych.

Tematyka analizy sprawozdań finansowych została wybrana świadomie. Zamiast tworzyć kolejny prosty projekt demonstracyjny, celem było zbudowanie aplikacji rozwiązującej rzeczywisty problem biznesowy oraz umożliwiającej dalszy rozwój w kierunku analizy danych finansowych, oceny przedsiębiorstw oraz wykorzystania narzędzi Data Science i sztucznej inteligencji.

Projekt został zaprojektowany jako długoterminowy. Kolejne etapy jego rozwoju będą obejmować rozbudowę modułów analitycznych, rozwój REST API, wdrażanie nowych technologii oraz rozszerzanie funkcjonalności wraz z kolejnymi kursami i zdobywanym doświadczeniem.

---

# Cele projektu

Podstawowym celem projektu było stworzenie nowoczesnej aplikacji webowej w Django, która umożliwia zarządzanie przedsiębiorstwami oraz import i analizę sprawozdań finansowych zapisanych w formacie XML.

Projekt miał również umożliwić praktyczne wykorzystanie technologii poznawanych podczas kursu Python Developer. Zamiast tworzyć kilka niezależnych, niewielkich aplikacji, od początku rozwijany był jeden większy projekt, który z każdą kolejną funkcjonalnością stawał się bardziej kompletny.

Najważniejsze cele projektu:

- stworzenie wieloużytkownikowej aplikacji webowej,
- zapewnienie pełnej izolacji danych użytkowników,
- import sprawozdań finansowych z plików XML,
- wykorzystanie relacyjnej bazy danych PostgreSQL,
- przygotowanie REST API z wykorzystaniem Django REST Framework,
- zastosowanie uwierzytelniania JWT,
- wdrożenie aplikacji na platformie Railway,
- przygotowanie automatycznych testów z wykorzystaniem pytest,
- stworzenie projektu stanowiącego profesjonalne portfolio Python Developera.

> **Dlaczego takie podejście?**

> Celem nie było jedynie zaliczenie kursu, ale zbudowanie projektu, który będzie rozwijany również po jego zakończeniu i stanie się podstawą do dalszej nauki oraz prezentacji umiejętności podczas rozmów kwalifikacyjnych.

---

# Najważniejsze funkcjonalności

Obecnie aplikacja umożliwia między innymi:

## Zarządzanie użytkownikami

- rejestrację użytkowników,
- logowanie i wylogowanie,
- pełną izolację danych pomiędzy użytkownikami,
- zabezpieczenie dostępu do danych z wykorzystaniem mechanizmów Django.

## Zarządzanie przedsiębiorstwami

- dodawanie, edycję i usuwanie przedsiębiorstw,
- przypisywanie przedsiębiorstw do właściciela konta,
- przypisywanie branż do przedsiębiorstw,
- prowadzenie profilu firmy zawierającego dodatkowe informacje.

## Sprawozdania finansowe

- import sprawozdań finansowych z plików XML,
- automatyczne odczytywanie danych z dokumentów,
- przechowywanie wielu sprawozdań dla jednej firmy,
- archiwizację i przywracanie sprawozdań.

## Komunikacja

- przygotowywanie mailingów,
- historię wysłanych wiadomości,
- zarządzanie korespondencją z poziomu aplikacji.

## REST API

- udostępnienie danych poprzez Django REST Framework,
- uwierzytelnianie z wykorzystaniem JWT,
- dokumentację API w Swagger UI i ReDoc.

## Jakość projektu

- automatyczne testy przygotowane z wykorzystaniem pytest,
- relacyjna baza danych PostgreSQL,
- obsługa zadań asynchronicznych z wykorzystaniem Celery i Redis,
- konteneryzacja z użyciem Dockera,
- wdrożenie produkcyjne na platformie Railway.

> **Dlaczego ten rozdział jest ważny?**
>
> Pokazuje on nie tylko zastosowane technologie, ale przede wszystkim możliwości aplikacji. Dzięki temu czytelnik już na początku dokumentacji może szybko zorientować się, jaki zakres funkcjonalności został zrealizowany w projekcie.

---

# Architektura aplikacji

Projekt został zbudowany zgodnie z architekturą Model–View–Template (MVT), wykorzystywaną przez framework Django. Poszczególne elementy aplikacji zostały rozdzielone zgodnie z ich odpowiedzialnością, co ułatwia rozwój projektu, testowanie oraz późniejsze utrzymanie kodu.

Najważniejsze elementy architektury:

- **Modele (Models)** – odpowiadają za przechowywanie danych w bazie PostgreSQL oraz relacje pomiędzy obiektami.
- **Widoki (Views)** – realizują logikę biznesową aplikacji i przetwarzają żądania użytkowników.
- **Szablony (Templates)** – odpowiadają za prezentację danych w interfejsie użytkownika.
- **REST API** – udostępnia dane aplikacji w formacie JSON z wykorzystaniem Django REST Framework.
- **Baza danych PostgreSQL** – przechowuje dane użytkowników, przedsiębiorstw, sprawozdań finansowych oraz pozostałych elementów systemu.
- **Celery i Redis** – obsługują wykonywanie zadań asynchronicznych.
- **Railway** – umożliwia wdrożenie aplikacji w środowisku produkcyjnym.

Architektura została zaprojektowana w taki sposób, aby umożliwić dalszy rozwój projektu bez konieczności przebudowy jego podstawowych elementów.

> **Dlaczego taka architektura?**
>
> Zastosowanie wzorca MVT oraz podział odpowiedzialności pomiędzy poszczególne komponenty ułatwia rozwój projektu, zwiększa czytelność kodu i pozwala łatwiej dodawać nowe funkcjonalności.

---

# Model danych

Podstawą aplikacji jest relacyjna baza danych PostgreSQL. Model danych został zaprojektowany z myślą o skalowalności aplikacji, łatwym rozszerzaniu jej funkcjonalności oraz zachowaniu pełnej izolacji danych pomiędzy użytkownikami.

Najważniejsze modele wykorzystywane w aplikacji:

- **User** – użytkownik systemu.
- **Firma** – przedsiębiorstwo należące do użytkownika.
- **SprawozdanieFinansowe** – dane finansowe przedsiębiorstwa za wybrany rok.
- **Branza** – klasyfikacja branż przedsiębiorstw.
- **ProfilFirmy** – dodatkowe informacje o przedsiębiorstwie.
- **Mailing** – historia przygotowanych wiadomości.

Relacje pomiędzy modelami zostały zaprojektowane zgodnie z zasadami relacyjnych baz danych i wykorzystują klucze obce (ForeignKey), relacje jeden-do-jednego (OneToOneField) oraz wiele-do-wielu (ManyToManyField).

Najważniejszym założeniem projektu jest pełna izolacja danych użytkowników. Każdy użytkownik ma dostęp wyłącznie do własnych przedsiębiorstw, sprawozdań finansowych oraz pozostałych danych zapisanych w systemie.

> **Dlaczego model danych jest ważny?**
>
> Odpowiednio zaprojektowana struktura bazy danych stanowi fundament całej aplikacji i umożliwia jej dalszy rozwój bez konieczności przebudowy istniejących modeli.

---

# Import sprawozdań finansowych XML

Jedną z najważniejszych funkcjonalności aplikacji jest import sprawozdań finansowych zapisanych w formacie XML pochodzących z systemu PRS/KRS.

Proces importu został zaprojektowany w taki sposób, aby maksymalnie uprościć pracę użytkownika. Po wskazaniu pliku XML aplikacja automatycznie odczytuje najważniejsze informacje dotyczące przedsiębiorstwa oraz dane finansowe zawarte w dokumencie.

Podczas importu wykonywane są między innymi następujące operacje:

- odczyt danych przedsiębiorstwa,
- identyfikacja firmy na podstawie numerów NIP i KRS,
- odczyt roku sprawozdawczego,
- import wybranych danych finansowych,
- zapis informacji w relacyjnej bazie PostgreSQL,
- wykrywanie istniejących sprawozdań i ochrona przed tworzeniem niepotrzebnych duplikatów.

Import XML stanowi podstawę dalszej analizy przedsiębiorstw i umożliwia sukcesywne rozbudowywanie aplikacji o kolejne moduły analityczne.

> **Dlaczego import XML jest ważny?**
>
> Automatyczne odczytywanie danych znacząco ogranicza liczbę operacji wykonywanych ręcznie, zmniejsza ryzyko błędów oraz pozwala szybciej rozpocząć analizę sytuacji finansowej przedsiębiorstwa.

---

# Bezpieczeństwo i izolacja danych użytkowników

Projekt od początku został zaprojektowany jako aplikacja wieloużytkownikowa. Jednym z podstawowych założeń było zapewnienie pełnej izolacji danych pomiędzy użytkownikami systemu.

Każdy użytkownik posiada własne przedsiębiorstwa, sprawozdania finansowe, profile firm oraz historię mailingów. Dane jednego użytkownika nie są widoczne dla pozostałych użytkowników aplikacji.

W projekcie wykorzystano między innymi następujące mechanizmy bezpieczeństwa:

- uwierzytelnianie użytkowników z wykorzystaniem systemu Django Authentication,
- autoryzację dostępu do widoków,
- filtrowanie danych na podstawie właściciela konta,
- ochronę przed dostępem do danych innych użytkowników,
- zabezpieczenie REST API z wykorzystaniem tokenów JWT,
- wykorzystanie mechanizmów bezpieczeństwa dostępnych w Django.

Dodatkowo aplikacja została przygotowana do pracy w środowisku produkcyjnym poprzez zastosowanie bezpiecznej konfiguracji HTTPS oraz odpowiednich ustawień bezpieczeństwa frameworka Django.

> **Dlaczego bezpieczeństwo było jednym z priorytetów?**
>
> Dane finansowe przedsiębiorstw mają charakter poufny. Dlatego od początku projektu wszystkie funkcjonalności były projektowane z uwzględnieniem kontroli dostępu oraz izolacji danych pomiędzy użytkownikami.

---

# REST API

Aplikacja udostępnia również interfejs REST API zbudowany z wykorzystaniem Django REST Framework. Dzięki temu dane mogą być wykorzystywane nie tylko przez interfejs webowy, ale również przez aplikacje mobilne, systemy zewnętrzne oraz inne usługi komunikujące się z API.

Najważniejsze możliwości REST API:

- pobieranie listy przedsiębiorstw,
- przeglądanie szczegółów przedsiębiorstwa,
- dostęp do sprawozdań finansowych,
- wyszukiwanie danych,
- uwierzytelnianie z wykorzystaniem tokenów JWT.

Projekt wykorzystuje Django REST Framework oraz bibliotekę Simple JWT, dzięki czemu API spełnia współczesne standardy bezpieczeństwa i może być rozwijane o kolejne endpointy.

Do dokumentowania API wykorzystano Swagger UI oraz ReDoc, co ułatwia testowanie oraz integrację z innymi aplikacjami.

> **Dlaczego REST API jest ważne?**
>
> Oddzielenie warstwy backendowej od klientów korzystających z danych umożliwia dalszy rozwój projektu, integrację z aplikacjami mobilnymi oraz tworzenie nowych usług opartych o te same dane.

---

# Testy automatyczne

Projekt posiada zestaw automatycznych testów przygotowanych z wykorzystaniem frameworka **pytest** oraz integracji **pytest-django**.

Aktualny zestaw obejmuje **45 testów automatycznych** rozmieszczonych w 12 modułach testowych.

Testy obejmują najważniejsze elementy aplikacji:

### Uwierzytelnianie użytkowników

Sprawdzane są między innymi:

- poprawne logowanie użytkownika,
- odrzucenie nieprawidłowego hasła,
- rejestracja nowego użytkownika.

### Izolacja danych i zarządzanie firmami

Testy weryfikują:

- tworzenie przedsiębiorstwa przez właściciela konta,
- widoczność wyłącznie własnych przedsiębiorstw,
- brak dostępu do danych innego użytkownika,
- wyszukiwanie i filtrowanie firm,
- usuwanie przedsiębiorstw,
- usuwanie powiązanych sprawozdań finansowych.

### Profile firm i branże

Testowane są między innymi:

- tworzenie i edycja profilu przedsiębiorstwa,
- relacja przedsiębiorstwa z wieloma branżami,
- prezentacja danych profilu,
- numer telefonu i strona internetowa,
- ochrona profilu przed edycją przez innego użytkownika,
- walidacja plików logo i bannerów,
- ograniczenie rozmiaru przesyłanych plików,
- zachowanie istniejącego logo podczas aktualizacji innych danych profilu.

### Sprawozdania finansowe

Testy obejmują:

- tworzenie sprawozdania finansowego,
- oznaczanie sprawozdania jako zarchiwizowanego,
- archiwizację,
- przywracanie sprawozdania z archiwum.

### Import XML

Mechanizm importu XML jest testowany między innymi pod kątem:

- odrzucenia nieprawidłowego pliku XML,
- tworzenia sprawozdania dla istniejącej firmy,
- ochrony przed utworzeniem duplikatu podczas ponownego importu,
- aktualizacji danych finansowych odczytanych z XML,
- automatycznego utworzenia nowej firmy i sprawozdania,
- ochrony przed przypisaniem sprawozdania do firmy należącej do innego użytkownika.

### Mailing

Testy sprawdzają:

- tworzenie mailingu,
- izolację historii mailingów pomiędzy użytkownikami.

### REST API i JWT

Testy API obejmują między innymi:

- wymaganie uwierzytelnienia,
- izolację danych użytkowników w REST API,
- ochronę szczegółów firmy należącej do innego użytkownika,
- prezentację profilu przedsiębiorstwa i branż,
- wyszukiwanie firm poprzez API,
- listę sprawozdań finansowych,
- uzyskiwanie tokenów JWT,
- odświeżanie tokenów JWT,
- dostęp do API z poprawnym tokenem,
- odrzucenie nieprawidłowego hasła,
- odrzucenie wygasłego tokenu JWT.

Aktualną liczbę i listę testów można sprawdzić poleceniem:

```bash
pytest --collect-only -q
```

Uruchomienie wszystkich testów:

```bash
pytest
```

W środowisku Docker Compose, po uruchomieniu kontenerów:

```bash
docker compose exec web pytest
```

Aktualnie pełny zestaw testów kończy się wynikiem:

```text
45 passed
```

> **Dlaczego testy są ważne?**
>
> Automatyczne testy chronią kluczowe funkcjonalności aplikacji przed regresją, pozwalają bezpieczniej rozwijać projekt oraz potwierdzają poprawność mechanizmów szczególnie istotnych dla systemu, takich jak izolacja danych użytkowników, import XML, REST API i uwierzytelnianie JWT.

---

# Deployment

Aplikacja została przygotowana do wdrożenia produkcyjnego oraz uruchomiona na platformie Railway.

Podczas przygotowania środowiska produkcyjnego wykorzystano między innymi:

- PostgreSQL jako produkcyjną bazę danych,
- Docker do konteneryzacji aplikacji,
- Railway jako platformę hostingową,
- konfigurację zmiennych środowiskowych,
- obsługę plików statycznych i multimedialnych,
- bezpieczną konfigurację HTTPS,
- konfigurację reverse proxy,
- ustawienia bezpieczeństwa Django dla środowiska produkcyjnego.

Dzięki zastosowaniu platformy Railway aplikacja może być uruchamiana w środowisku zbliżonym do produkcyjnego i jest dostępna przez przeglądarkę internetową.

> **Dlaczego deployment jest ważny?**
>
> Wdrożenie aplikacji pokazuje, że projekt nie kończy się na kodzie źródłowym. Gotowa aplikacja może zostać uruchomiona i przetestowana przez użytkowników w rzeczywistym środowisku.

---

# Docker

Projekt został przygotowany do uruchamiania z wykorzystaniem kontenerów Docker. Dzięki temu aplikacja może być uruchamiana w powtarzalnym środowisku niezależnie od systemu operacyjnego.

Zastosowanie Dockera umożliwia:

- łatwiejszą konfigurację środowiska,
- uproszczenie procesu wdrażania,
- uruchamianie wszystkich usług w spójnej konfiguracji,
- ograniczenie problemów wynikających z różnic pomiędzy środowiskami programistycznymi.

Do uruchamiania wielu usług wykorzystano również **Docker Compose**, co upraszcza konfigurację środowiska deweloperskiego oraz proces wdrażania aplikacji.

Konteneryzacja ułatwia również dalszy rozwój projektu oraz jego wdrażanie na kolejnych platformach hostingowych.

> **Dlaczego Docker jest ważny?**
>
> Dzięki konteneryzacji aplikacja działa w przewidywalnym środowisku, co zwiększa stabilność wdrożeń oraz ułatwia współpracę z innymi programistami.

---

# Celery i zadania asynchroniczne

W projekcie wykorzystano bibliotekę **Celery** wraz z brokerem wiadomości **Redis** do wykonywania zadań asynchronicznych.

Obecnie mechanizm ten został zastosowany do obsługi wysyłki mailingów. Dzięki temu proces wysyłania wiadomości odbywa się w tle i nie blokuje działania aplikacji ani interfejsu użytkownika.

Najważniejsze możliwości zastosowanego rozwiązania:

- asynchroniczna wysyłka mailingów,
- wykonywanie długotrwałych operacji poza głównym procesem aplikacji,
- zwiększenie płynności działania interfejsu użytkownika,
- możliwość dalszej rozbudowy projektu o kolejne zadania wykonywane w tle,
- wykorzystanie Redis jako brokera komunikatów pomiędzy Django i Celery.

Zastosowanie Celery przygotowuje projekt do dalszego rozwoju i umożliwia łatwe dodawanie kolejnych zadań wykonywanych asynchronicznie. W przyszłości mechanizm ten może zostać wykorzystany między innymi do generowania raportów, importu danych oraz wysyłania powiadomień.

> **Dlaczego Celery jest ważne?**
>
> Wykonywanie czasochłonnych operacji w tle zwiększa wydajność aplikacji, poprawia komfort pracy użytkownika oraz umożliwia łatwe dodawanie kolejnych zadań asynchronicznych w przyszłości.

---

# Responsywność aplikacji

Aplikacja została przygotowana do wygodnej pracy zarówno na komputerach, jak i urządzeniach mobilnych. Interfejs użytkownika został zaprojektowany zgodnie z zasadami Responsive Web Design (RWD), dzięki czemu automatycznie dostosowuje się do różnych rozdzielczości ekranu.

Podczas prac nad responsywnością dostosowano między innymi:

- formularze logowania i rejestracji,
- widoki przedsiębiorstw,
- tabele ze sprawozdaniami finansowymi,
- formularze importu XML,
- moduł mailingu,
- archiwum sprawozdań,
- panel administracyjny oraz pozostałe elementy interfejsu użytkownika.

Celem wprowadzonych zmian było zapewnienie wygodnej obsługi aplikacji zarówno na komputerach, tabletach, jak i smartfonach.

> **Dlaczego responsywność jest ważna?**
>
> Współczesne aplikacje internetowe powinny działać poprawnie na różnych urządzeniach. Responsywny interfejs zwiększa komfort użytkowania oraz pozwala korzystać z aplikacji niezależnie od wielkości ekranu.

---

# Historia rozwoju projektu

Projekt jest rozwijany etapowo od lutego 2026 roku. Kolejne funkcjonalności były dodawane stopniowo wraz z rozwojem aplikacji, zdobywaniem nowych umiejętności oraz rozszerzaniem pierwotnych założeń projektu.

Najważniejsze etapy rozwoju aplikacji:

### Luty 2026 – rozpoczęcie projektu

- utworzenie projektu Django i aplikacji `firmy_django`,
- przygotowanie podstawowej struktury projektu,
- konfiguracja zależności,
- przejście z SQLite na PostgreSQL,
- uporządkowanie repozytorium i konfiguracji `.gitignore`.

### Maj–czerwiec 2026 – podstawowe funkcjonalności aplikacji

- rozwój modeli przedsiębiorstw i sprawozdań finansowych,
- wyszukiwanie i filtrowanie przedsiębiorstw,
- sortowanie danych,
- prezentacja należności i danych finansowych,
- rozwój modułu mailingu,
- wysyłka wiadomości e-mail przez SMTP,
- historia wysłanych mailingów.

### Czerwiec 2026 – użytkownicy, bezpieczeństwo danych i XML

- rejestracja i logowanie użytkowników,
- walidacja haseł,
- izolacja danych pomiędzy użytkownikami,
- import sprawozdań finansowych XML pobieranych z PRS,
- identyfikacja przedsiębiorstw na podstawie danych z XML,
- obsługa wielu sprawozdań finansowych dla jednego przedsiębiorstwa,
- archiwizacja i przywracanie sprawozdań,
- usuwanie przedsiębiorstw,
- rozwój zestawu testów automatycznych.

### Lipiec 2026 – rozbudowa architektury aplikacji

- dodanie profilu przedsiębiorstwa,
- obsługa branż przedsiębiorstw,
- możliwość dodawania logo i bannerów,
- rozwój REST API,
- uwierzytelnianie JWT dla API,
- dokumentacja API za pomocą Swagger/OpenAPI,
- dalsza rozbudowa testów,
- refaktoryzacja mechanizmu importu XML,
- dodanie asynchronicznej wysyłki mailingów za pomocą Celery i Redis,
- przygotowanie konfiguracji Docker i Docker Compose,
- przygotowanie aplikacji do deploymentu.

### Sierpień 2026 – przygotowanie wersji portfolio

- rozbudowa responsywności interfejsu użytkownika,
- dostosowanie formularzy, tabel i pozostałych widoków do urządzeń mobilnych,
- poprawa dostępności wybranych elementów aplikacji,
- przeniesienie testów do pytest,
- poprawa konfiguracji bezpieczeństwa środowiska produkcyjnego,
- konfiguracja obsługi HTTPS za reverse proxy,
- rozbudowa dokumentacji projektu.

Projekt jest nadal rozwijany. Obecna wersja stanowi fundament pod kolejne moduły związane z analizą finansową przedsiębiorstw, oceną ich kondycji finansowej, analizą należności oraz wspomaganiem procesów związanych z oceną kontrahentów i decyzjami finansowymi.

Dalszy rozwój projektu może obejmować między innymi rozbudowane wskaźniki finansowe, scoring przedsiębiorstw, raporty i dashboardy, automatyzację analizy danych oraz wykorzystanie metod Data Science i sztucznej inteligencji.

---

# Technologie

Projekt wykorzystuje zestaw technologii obejmujących backend aplikacji, bazę danych, REST API, zadania asynchroniczne, testy, konteneryzację oraz deployment.

### Backend

- **Python** – główny język programowania aplikacji,
- **Django** – framework wykorzystywany do budowy aplikacji webowej,
- **Django REST Framework** – tworzenie REST API aplikacji.

### Baza danych

- **PostgreSQL** – główna relacyjna baza danych wykorzystywana przez aplikację,
- **Django ORM** – obsługa modeli oraz komunikacji aplikacji z bazą danych.

### REST API

- **Django REST Framework** – udostępnianie danych poprzez REST API,
- **JWT (JSON Web Token)** – uwierzytelnianie użytkowników korzystających z API,
- **Swagger / OpenAPI** – dokumentacja oraz możliwość testowania endpointów API.

### Zadania asynchroniczne

- **Celery** – wykonywanie zadań asynchronicznych,
- **Redis** – broker komunikatów wykorzystywany przez Celery.

Obecnie zadania asynchroniczne wykorzystywane są między innymi do wysyłania mailingów w tle.

### Testy

- **pytest** – uruchamianie i organizacja testów automatycznych,
- **pytest-django** – integracja pytest z aplikacją Django.

Testy obejmują między innymi logowanie i rejestrację użytkowników, izolację danych, obsługę przedsiębiorstw, profile firm, import XML, sprawozdania finansowe, archiwizację oraz REST API.

### Konteneryzacja

- **Docker** – konteneryzacja aplikacji,
- **Docker Compose** – konfiguracja i uruchamianie wielu usług wymaganych przez aplikację.

### Deployment i środowisko produkcyjne

- **Railway** – platforma wykorzystywana do deploymentu aplikacji,
- **Gunicorn** – serwer WSGI wykorzystywany do uruchamiania Django w środowisku produkcyjnym,
- obsługa **HTTPS za reverse proxy**,
- konfiguracja ustawień bezpieczeństwa dla środowiska produkcyjnego.

### Frontend

- **HTML5**,
- **CSS3**,
- **Django Templates**,
- **Responsive Web Design (RWD)**.

Interfejs został dostosowany do pracy na komputerach, tabletach i urządzeniach mobilnych.

### Narzędzia developerskie

- **Git** – system kontroli wersji,
- **GitHub** – repozytorium kodu oraz historia rozwoju projektu,
- **WSL / Linux** – środowisko wykorzystywane podczas tworzenia aplikacji.

Zastosowany zestaw technologii pozwala rozwijać projekt zarówno jako aplikację portfolio, jak również jako fundament większego systemu do analizy danych finansowych przedsiębiorstw.

---

# Struktura projektu

Projekt został podzielony na główną aplikację Django, konfigurację projektu oraz katalogi i pliki odpowiadające za testy, dane, konteneryzację i uruchamianie poszczególnych usług.

Najważniejsze elementy struktury projektu:

```text
projekt_django/
├── firmy_django/
│   ├── management/
│   ├── migrations/
│   ├── templates/
│   ├── templatetags/
│   ├── tests/
│   ├── admin.py
│   ├── api_urls.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── urls.py
│   └── views.py
│
├── projekt_django/
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── sprawozdania_xml/
├── static/
├── templates/
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pytest.ini
├── requirements.txt
└── README_PL.md

```

### Główna aplikacja `firmy_django`

Katalog `firmy_django/` zawiera podstawową logikę biznesową aplikacji:

- **models.py** – modele danych aplikacji,
- **views.py** – widoki i logika obsługi żądań,
- **forms.py** – formularze Django,
- **serializers.py** – serializery wykorzystywane przez REST API,
- **api_urls.py** – routing endpointów REST API,
- **urls.py** – routing głównej aplikacji,
- **admin.py** – konfiguracja panelu administracyjnego Django,
- **tasks.py** – zadania asynchroniczne wykonywane przez Celery,
- **tests/** – testy automatyczne przygotowane z wykorzystaniem pytest,
- **migrations/** – migracje bazy danych,
- **templates/** – szablony HTML aplikacji,
- **management/** – własne polecenia zarządzające Django.

### Konfiguracja projektu `projekt_django`

Katalog `projekt_django/` zawiera konfigurację całego projektu:

- **settings.py** – główne ustawienia Django i konfiguracja środowiska,
- **urls.py** – główny routing projektu,
- **celery.py** – konfiguracja Celery,
- **wsgi.py** – punkt wejścia dla aplikacji WSGI,
- **asgi.py** – punkt wejścia dla aplikacji ASGI.

### Pozostałe elementy

- **media/** – katalog tworzony lokalnie dla plików przesyłanych przez użytkowników; nie jest przechowywany w repozytorium,
- **staticfiles/** – katalog generowany podczas `collectstatic` na potrzeby środowiska produkcyjnego; nie jest przechowywany w repozytorium,
- **sprawozdania_xml/** – pliki XML wykorzystywane podczas importu sprawozdań finansowych,
- **static/** – źródłowe pliki statyczne aplikacji,
- **Dockerfile** – definicja obrazu Docker aplikacji,
- **docker-compose.yml** – konfiguracja usług uruchamianych za pomocą Docker Compose,
- **pytest.ini** – konfiguracja frameworka pytest,
- **requirements.txt** – lista zależności projektu,
- **manage.py** – narzędzie administracyjne Django.

> **Dlaczego struktura projektu jest ważna?**
>
> Czytelny podział odpowiedzialności pomiędzy poszczególne moduły ułatwia rozwój aplikacji, testowanie, utrzymanie kodu oraz szybkie odnalezienie elementów odpowiedzialnych za konkretną funkcjonalność.

---

# Instalacja i uruchomienie projektu

Najprostszym sposobem uruchomienia kompletnego środowiska aplikacji jest wykorzystanie Docker Compose. Pozwala to uruchomić Django, PostgreSQL, Redis oraz Celery bez ręcznej konfiguracji poszczególnych usług.

## Wymagania

Przed uruchomieniem projektu należy posiadać:

- Git,
- Docker,
- Docker Compose.

## 1. Klonowanie repozytorium

```bash
git clone https://github.com/Stazus/projekt_django.git
cd projekt_django
```

## 2. Budowa i uruchomienie kontenerów

```bash
docker compose up -d --build
```

Docker Compose uruchamia następujące usługi:

- **web** – aplikacja Django,
- **db** – PostgreSQL 16,
- **redis** – broker wiadomości Redis,
- **celery** – worker Celery.

## 3. Wykonanie migracji bazy danych

Po uruchomieniu kontenerów należy wykonać migracje:

```bash
docker compose exec web python manage.py migrate
```

## 4. Utworzenie administratora

Aby uzyskać dostęp do panelu administracyjnego Django, można utworzyć konto superusera:

```bash
docker compose exec web python manage.py createsuperuser
```

Następnie należy podać nazwę użytkownika, adres e-mail oraz hasło administratora.

## 5. Uruchomienie aplikacji

Po uruchomieniu kontenerów aplikacja jest dostępna pod adresem:

```text
http://localhost:8000/
```

Panel administracyjny Django:

```text
http://localhost:8000/admin/
```

## 6. REST API i dokumentacja

REST API aplikacji jest dostępne pod prefiksem:

```text
http://localhost:8000/api/
```

Dokumentacja Swagger UI:

```text
http://localhost:8000/api/docs/
```

Dokumentacja ReDoc:

```text
http://localhost:8000/api/redoc/
```

## 7. Uruchomienie testów

Testy automatyczne można uruchomić poleceniem:

```bash
docker compose exec web pytest
```

## 8. Zatrzymanie środowiska

```bash
docker compose down
```

Dane PostgreSQL są przechowywane w wolumenie `postgres_data`, dzięki czemu nie są usuwane przy zwykłym zatrzymaniu kontenerów.

> **Dlaczego Docker Compose jest zalecanym sposobem uruchomienia projektu?**
>
> Projekt wykorzystuje kilka współpracujących usług: Django, PostgreSQL, Redis oraz Celery. Docker Compose pozwala uruchomić całe środowisko w spójnej konfiguracji bez konieczności ręcznej instalacji i konfigurowania każdej z nich osobno.

---

# Panel administratora Django

Projekt wykorzystuje wbudowany panel administracyjny Django do zarządzania danymi systemu przez administratora.

W panelu administracyjnym zarejestrowane są między innymi następujące modele:

- **Firmy**,
- **Sprawozdania finansowe**,
- **Mailingi**,
- **Branże**,
- **Profile firm**.

Panel administratora został dostosowany tak, aby ułatwić pracę z większą liczbą danych.

### Zarządzanie firmami

Dla modelu `Firma` dostępne są między innymi:

- lista firm z najważniejszymi danymi,
- wyszukiwanie po nazwie, NIP-ie, e-mailu, REGON-ie oraz opisie źródła e-maila,
- filtrowanie po mieście,
- podgląd i edycja sprawozdań finansowych bezpośrednio z poziomu firmy.

### Zarządzanie sprawozdaniami finansowymi

Administrator może przeglądać między innymi:

- rok sprawozdania,
- należności,
- aktywa,
- przychody,
- zysk netto.

Dostępne jest również wyszukiwanie po danych firmy oraz filtrowanie sprawozdań według roku.

### Zarządzanie mailingami

Panel administratora umożliwia przeglądanie historii mailingów wraz z informacjami takimi jak:

- temat wiadomości,
- liczba odbiorców,
- data wysłania.

Dostępne jest również wyszukiwanie po temacie i treści wiadomości oraz filtrowanie po dacie wysłania.

### Uprawnienia administratora

Dostęp do panelu administracyjnego mają wyłącznie użytkownicy posiadający odpowiednie uprawnienia Django Staff lub Superuser.

Administrator może zarządzać danymi aplikacji niezależnie od standardowego interfejsu użytkownika. Panel Django Admin pełni rolę narzędzia administracyjnego i nie zastępuje właściwego interfejsu biznesowego aplikacji.

Panel administratora jest dostępny pod adresem:

```text
/admin/
```

> **Dlaczego Django Admin jest ważny?**
>
> Wbudowany panel administracyjny pozwala szybko zarządzać danymi systemu, użytkownikami i uprawnieniami bez konieczności tworzenia osobnego interfejsu administracyjnego od podstaw.

---

# Konfiguracja i zmienne środowiskowe

Aplikacja wykorzystuje zmienne środowiskowe do przechowywania ustawień zależnych od środowiska uruchomieniowego oraz danych, które nie powinny być zapisywane bezpośrednio w kodzie źródłowym.

Najważniejsze obsługiwane zmienne środowiskowe:

- **SECRET_KEY** – klucz bezpieczeństwa Django; w środowisku produkcyjnym musi być ustawiony jawnie,
- **DEBUG** – określa tryb pracy aplikacji (`True` dla środowiska deweloperskiego, `False` dla produkcyjnego),
- **ALLOWED_HOSTS** – lista hostów, z których aplikacja może przyjmować żądania,
- **CSRF_TRUSTED_ORIGINS** – lista zaufanych źródeł używanych przez mechanizmy ochrony CSRF,
- **DATABASE_URL** – adres połączenia z bazą danych wykorzystywany między innymi w środowisku produkcyjnym,
- **EMAIL_HOST_USER** – nazwa użytkownika konta SMTP,
- **EMAIL_HOST_PASSWORD** – hasło do konta SMTP,
- **REDIS_URL** – adres serwera Redis wykorzystywanego przez Celery.

Konfiguracja Celery korzysta z tej samej wartości `REDIS_URL` zarówno jako brokera wiadomości, jak i backendu wyników:

```text
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

```
W środowisku Docker aplikacja korzysta z Redis dostępnego pod adresem:

```text
redis://redis:6379/0
```

natomiast podczas lokalnego uruchomienia poza Dockerem domyślnie wykorzystywany jest:

```text
redis://localhost:6379/0
```

W trybie deweloperskim projekt może korzystać z lokalnego klucza `SECRET_KEY`, jednak przy `DEBUG=False` jego brak powoduje błąd konfiguracji. Dzięki temu uruchomienie środowiska produkcyjnego bez jawnie ustawionego klucza bezpieczeństwa jest blokowane.

> **Dlaczego zmienne środowiskowe są ważne?**
>
> Oddzielenie konfiguracji od kodu źródłowego zwiększa bezpieczeństwo projektu, ułatwia wdrażanie aplikacji w różnych środowiskach i pozwala uniknąć zapisywania poufnych danych, takich jak hasła SMTP czy produkcyjny `SECRET_KEY`, w repozytorium Git.

---

# Dalszy rozwój projektu

Projekt został zaprojektowany jako aplikacja rozwijana długoterminowo. Obecna wersja stanowi funkcjonalną podstawę systemu do zarządzania danymi przedsiębiorstw oraz ich sprawozdaniami finansowymi, która może być stopniowo rozszerzana o kolejne moduły analityczne.

Planowane kierunki dalszego rozwoju obejmują między innymi:

- rozbudowę zakresu danych finansowych odczytywanych ze sprawozdań,
- obliczanie wskaźników finansowych przedsiębiorstw,
- analizę zmian sytuacji finansowej firmy w kolejnych latach,
- ocenę kondycji finansowej przedsiębiorstw,
- tworzenie systemu scoringowego,
- wspomaganie oceny wiarygodności kontrahentów,
- wspomaganie decyzji związanych z finansowaniem i faktoringiem,
- tworzenie raportów i dashboardów,
- wizualizację danych finansowych,
- automatyzację procesów analitycznych.

W dalszych etapach rozwoju planowane jest również wykorzystanie metod **Data Science**, uczenia maszynowego oraz sztucznej inteligencji. Pozwoli to między innymi na automatyczne wykrywanie zależności w danych, porównywanie przedsiębiorstw oraz generowanie podsumowań i rekomendacji wspierających analizę finansową.

Docelowo projekt może rozwijać się w kierunku rozbudowanej platformy wspomagającej analizę przedsiębiorstw dla analityków finansowych, firm faktoringowych, pośredników finansowych oraz innych użytkowników wykorzystujących dane finansowe przedsiębiorstw.

> **Dlaczego projekt będzie dalej rozwijany?**
>
> Projekt powstał nie tylko jako aplikacja portfolio, ale również jako praktyczna platforma do dalszej nauki i wdrażania kolejnych technologii. Dzięki modułowej architekturze nowe funkcjonalności mogą być dodawane stopniowo bez konieczności przebudowy podstaw systemu.

---

# Autor

**Stanisław Flak**

Projekt został stworzony w ramach nauki programowania w języku Python i frameworku Django oraz jest rozwijany jako projekt portfolio prezentujący praktyczne wykorzystanie technologii backendowych.

### Aplikacja online

Publiczna wersja aplikacji została wdrożona na platformie Railway:

https://projektdjango-production.up.railway.app/

### Repozytorium

Kod źródłowy projektu jest dostępny na GitHub:

[https://github.com/Stazus/projekt_django](https://github.com/Stazus/projekt_django)

Projekt jest nadal rozwijany wraz ze zdobywaniem kolejnych umiejętności z zakresu tworzenia aplikacji webowych, baz danych, REST API, testowania, DevOps, Data Science oraz sztucznej inteligencji.

---

> **Status projektu**
>
> Aplikacja jest aktywnie rozwijana. Aktualna wersja portfolio obejmuje między innymi Django, PostgreSQL, import danych finansowych XML, REST API, JWT, testy automatyczne, Celery, Redis, Docker oraz deployment produkcyjny na Railway.

---

# Licencja

Projekt jest udostępniany na warunkach licencji **MIT**.

Szczegółowe warunki znajdują się w pliku:

```text
LICENSE
```

Licencja MIT pozwala na używanie, kopiowanie, modyfikowanie i rozpowszechnianie kodu przy zachowaniu informacji o prawach autorskich i treści licencji.

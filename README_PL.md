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

Projekt został wyposażony w zestaw automatycznych testów przygotowanych z wykorzystaniem frameworka pytest.

Podczas rozwoju aplikacji przetestowano między innymi:

- uwierzytelnianie użytkowników,
- izolację danych pomiędzy użytkownikami,
- zarządzanie przedsiębiorstwami,
- import sprawozdań finansowych XML,
- archiwizację sprawozdań,
- mailing,
- REST API,
- profile przedsiębiorstw,
- bezpieczeństwo dostępu do danych.

W końcowym etapie projektu testy zostały uporządkowane i przeniesione z frameworka unittest do pytest, co pozwoliło uzyskać bardziej przejrzystą strukturę katalogów oraz łatwiejsze rozwijanie zestawu testów.

Automatyczne testy stanowią istotny element projektu i pozwalają szybko sprawdzić poprawność działania aplikacji po wprowadzeniu kolejnych zmian.

> **Dlaczego testy są ważne?**
>
> Automatyczne testowanie zwiększa jakość projektu, ogranicza ryzyko wprowadzania błędów oraz ułatwia dalszy rozwój aplikacji.

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

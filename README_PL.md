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

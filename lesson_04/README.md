# Практическая работа № 4. План запроса и индексы MongoDB

## 1. Цель работы

Изучить планы выполнения запросов MongoDB, научиться использовать команду `explain("executionStats")` и сравнить эффективность запросов с индексами и без них.

## 2. Описание работы

В ходе практической работы использовалась база данных `logs` и коллекция `events`, содержащая 1200 документов.

Для анализа запросов применялась команда `explain("executionStats")`. С её помощью можно узнать, сколько документов и ключей индекса проверила MongoDB, сколько документов вернула и какие этапы использовались при выполнении запроса.

## 3. Сравнение планов выполнения

| Файл | Используемый индекс | Найдено документов | Проверено документов | Проверено ключей индекса | Этапы плана |
|---|---|---:|---:|---:|---|
| `plan-1.json` | Без дополнительного индекса | 33 | 1200 | 0 | COLLSCAN → SORT |
| `plan-2.json` | `service, level, ts, duration_ms` | 33 | 33 | 43 | IXSCAN → FETCH |
| `plan-3a.json` | `duration_ms, service, level, ts` | 33 | 33 | 378 | IXSCAN → SORT → FETCH |
| `plan-3b.json` | `service, level, duration_ms, ts` | 33 | 33 | 33 | IXSCAN → SORT → FETCH |
| `plan-4-bez.json` | Без дополнительного индекса | 10 | 1200 | 0 | COLLSCAN → SORT |
| `plan-4.json` | `level, duration_ms` | 10 | 10 | 10 | IXSCAN → FETCH → LIMIT |

## 4. Анализ результатов

### 4.1. Запрос без индекса

В первом запросе MongoDB проверила все 1200 документов и нашла 33 подходящих записи. Для этого использовался этап `COLLSCAN`, после которого выполнялась сортировка `SORT`.

Это показывает, что без подходящего индекса базе данных приходится проверять всю коллекцию.

### 4.2. Индекс с полями точного совпадения и сортировки

Во втором запросе был создан индекс `{ service: 1, level: 1, ts: -1, duration_ms: 1 }`.

После его создания количество проверенных документов уменьшилось с 1200 до 33. Отдельная сортировка исчезла, поскольку индекс позволил получать записи в нужном порядке по полю `ts`.

### 4.3. Сравнение порядка полей индекса

В третьем задании проверялись два индекса с разным порядком полей.

В плане `plan-3a.json` было проверено 378 ключей индекса, а в `plan-3b.json` — 33. При этом в обоих случаях сохранился этап `SORT`.

Таким образом, порядок полей индекса влияет на количество проверяемых ключей и возможность выполнения сортировки непосредственно по индексу.

### 4.4. Запрос с ограничением результата

В последнем задании проверялся запрос, который возвращает 10 событий с уровнем `error`, отсортированных по убыванию длительности.

После создания индекса `{ level: 1, duration_ms: -1 }` MongoDB проверила только 10 ключей индекса и 10 документов. В плане появился этап `LIMIT`, а отдельная сортировка не потребовалась.

Для завершения сравнения необходимо сопоставить этот результат с планом без дополнительного индекса из файла `plan-4-bez.json`.

## 5. Ссылки на разбор планов

После загрузки каждого JSON-файла на сайт Paste the Plan необходимо вставить полученную ссылку в соответствующий пункт.

- `plan-1.json` — [Разбор_1](https://dfrancour.dev/tools/mongodb-paste-the-plan#v1:zVVtbxs3DP4vRD_egju_xMl9S_yyBY3nNJe1GIphoCX6olknXSWeY9fwfx8kv2Ztk6IDhn3ymeRDig8fSmugZa1RmffkvLIGcsgggU8NudWdRmPIQb4GgxX5GgVBDtqW_owWZNhDAspIWo6UZnIFMeQz1J4SqNF5ku9CmoB_g0ZC_nENmhako4U-QQ7knHWw2SRr8OQWKhTY-2pcVbFIdMvGIStr_qx8DCkZ8m6abjZ_bHbH_QX9I-TQv8463eHFABKoNZo-ikd6S6vnHluzqtTnmPFBVTRWWisPeZpAhcub0BPJiSusbkKIv6eQRh7aOwZdGflSVCHQ-Ac7XNbaSvpnwJMyRpkyEB2a8oxlYLiY3D9AAt46vkNmctHLHvKfsk0CFVW3qlIMeZZ2Lrq98zRNgFd1gHpV1ZriXOqGi23CY-b-5Pa26F_9CgnM4sz-g-FI5UjwVlsz657QyYACR3-RYJKhew_5xxBLSxKRy4KRY66jpRGCvIecXUMJmHvixplAZrt9AjydZisBtoz6La38cImViuHpzjqw4sSatQKLp_VL8l8Zyut1h55VhUyx0pN1cx-yt7sJoFygEXuoIZIBFWtn2_-_K9LbI3pcUCAhuANXnq07MSg_nIzi179SyZYIZCzUZyqs43C4y-wiS6DxJAfKzw9i9bXSersj8ZNkBLJ1WFLAR9f_R3c_Oqkwi29OKjvv_fCkvrYICcgvZLgJ2yFsVUV-1jBT4RcOV-6RwQM9R16SPZs7GpNvk7TVzjPRvJHT3Q0PwU1uQe7GzGwIerSeIQfR6YmpTNsSCcMdG1O0emnWS2BxeER6Z-lZJ7wkpeLj0yLoMu1StzvrSdnC7HImpp12b9ZLL88vWqLTaeF0mrXE-bH4HTqsiMnFsysTZI46visjFMTXzWxGLqjvesVhYU_E_mX0GJeThuuGB1a8jLm1dt7UUcc3wVSRVMg0sKIJPI9x-TJ-H1jYxgn62dmmHuNyTJV1q1dOOsbltbZirkwZNnKL-c1j-VqLd84-qqniPXpMrqSJGVtT2mK3nM_rXEn5YAvi7-2jIP6gjLRPo6B-_70djcIMw371rWFn9Vb_gvoavVdiaEplKMzcziHPNn8D)
- `plan-2.json` — [Разбор_2](https://dfrancour.dev/tools/mongodb-paste-the-plan)
- `plan-3a.json` — [Разбор_3a](https://dfrancour.dev/tools/mongodb-paste-the-plan)
- `plan-3b.json` — [Разбор_3b](https://dfrancour.dev/tools/mongodb-paste-the-plan)
- `plan-4-bez.json` — [Разбор_4-bez](https://dfrancour.dev/tools/mongodb-paste-the-plan)
- `plan-4.json` — [Разбор_4](https://dfrancour.dev/tools/mongodb-paste-the-plan)

Сайт: https://dfrancour.dev/tools/mongodb-paste-the-plan

## 6. Вывод

В ходе практической работы были изучены планы выполнения запросов MongoDB и проверено влияние индексов на производительность поиска и сортировки.

Результаты показали, что правильно подобранный составной индекс позволяет уменьшить количество проверяемых документов и избежать отдельной сортировки. Также было установлено, что порядок полей в индексе влияет на эффективность запроса.

Индексы необходимо подбирать с учётом условий фильтрации, сортировки и ограничений результата.
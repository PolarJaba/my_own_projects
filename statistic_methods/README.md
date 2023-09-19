# Статистическая обработка временных рядов

### Программа автоматически реализует следующие задачи:

1. Рассчет описательных статистик:

```
                               parameters                                       values
Станция                          STATION                                          29862
Период                           PERIOD  from 2022-06-01 00:00:00 to 2022-08-31 00:00:00
Среднее                          MEAN                                             18.0
Максимум                         MAX                                              27.9
Минимум                          MIN                                              10.2
Размах                           RANGE                                            17.7
Стандартное отклонение           STD                                              3.7
Дисперсия                        DISPERSION                                       13.8
Коэффициент вариации             VARIATION COEFFICIENT                            0.21
Коэффициент асимметрии           ASYMMETRY COEFFICIENT                            -0.1
Эксцесс                          EXCESS                                           -0.22
```

3. Запись полученных характеристик в [файл](https://github.com/PolarJaba/my_own_projects/blob/main/statistic_methods/stat_params_summer_2022.csv)
4. Построение графика временного хода ряда с нанесением на него основных статистик
5. Построение гистограммы
6. Построение графика обеспеченности

Полученные графические представления записываются в [файл](https://github.com/PolarJaba/my_own_projects/blob/main/statistic_methods/all_stat_graph.png).

### В результате получено представление о статистических характеристиках среднесуточных температур воздуха в г. Абакан за период июнь - август 2022 г.:

![graphs](https://github.com/PolarJaba/my_own_projects/blob/main/statistic_methods/all_stat_graph.png)
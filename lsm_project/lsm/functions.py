"""
В этом модуле хранятся функции для применения МНК
"""

from typing import Optional
from numbers import Real  # раскомментируйте при необходимости

from lsm_project.event_logger.event_logger import EventLogger

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)

PRECISION = 3  # константа для точности вывода
event_logger = EventLogger()  # для логирования


def get_lsm_description(
        abscissa: list[float],
        ordinates: list[float],
        mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL,
) -> LSMDescription:
    """
    Функции для получения описания рассчитаной зависимости

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: mismatch_strategy - стратегия обработки несовпадения

    :return: структура типа LSMDescription
    """

    global event_logger

    # ваш код
    # эту строчку можно менять

    if type(abscissa) is not list or type(ordinates) is not list:
        try:
            abscissa = list(abscissa)
            ordinates = list(ordinates)
        except TypeError:
            raise TypeError

    for i in abscissa + ordinates:
        if isinstance(i, Real) is False or min(len(ordinates), len(abscissa)) <= 2:
            raise ValueError

    if len(abscissa) != len(ordinates):
        if mismatch_strategy == MismatchStrategies.FALL:
            raise RuntimeError
        elif mismatch_strategy == MismatchStrategies.CUT:
            abscissa = abscissa[: max(len(abscissa), len(ordinates))]
            ordinates = ordinates[: max(len(abscissa), len(ordinates))]
        else:
            raise ValueError

    def samp_mean(x: list[float]) -> float:
        return sum(x) / len(x)

    n = len(ordinates)

    incline = (
                      sum([abscissa[i] * ordinates[i] for i in range(n)]) / n
                      - samp_mean(ordinates) * samp_mean(abscissa)
              ) / (samp_mean([i ** 2 for i in abscissa]) - samp_mean(abscissa) ** 2)

    shift = samp_mean(ordinates) - incline * samp_mean(abscissa)

    disp_y_sqr = (1 / (n - 2)) * sum(
        [(ordinates[i] - incline * abscissa[i] - shift) ** 2 for i in range(n)]
    )
    incline_error = (
                            disp_y_sqr
                            / (
                                    n
                                    * (
                                            samp_mean([abscissa[i] ** 2 for i in range(n)])
                                            - samp_mean(abscissa) ** 2
                                    )
                            )
                    ) ** 0.5
    shift_error = (
                          disp_y_sqr
                          * samp_mean([abscissa[i] ** 2 for i in range(n)])
                          / (
                                  n
                                  * (
                                          samp_mean([abscissa[i] ** 2 for i in range(n)])
                                          - samp_mean(abscissa) ** 2
                                  )
                          )
                  ) ** 0.5

    return LSMDescription(incline, shift, incline_error, shift_error)


def get_lsm_lines(
        abscissa: list[float],
        ordinates: list[float],
        lsm_description: Optional[LSMDescription] = None,
) -> LSMLines:
    """
    Функция для расчета значений функций с помощью результатов МНК

    :param: abscissa - значения абсцисс
    :param: ordinates - значение ординат
    :param: lsm_description - описание МНК

    :return: структура типа LSMLines
    """

    # ваш код
    # эту строчку можно менять

    if lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates)
    if isinstance(lsm_description, LSMDescription) is False:
        raise TypeError

    n = len(abscissa)
    incline = lsm_description.incline
    incline_error = lsm_description.incline_error
    shift = lsm_description.shift
    shift_error = lsm_description.shift_error

    line_predicted = [incline * abscissa[i] + shift for i in range(n)]
    line_above = [
        (incline + incline_error) * abscissa[i] + shift + shift_error for i in range(n)
    ]
    line_under = [
        (incline - incline_error) * abscissa[i] + shift - shift_error for i in range(n)
    ]

    return LSMLines(
        abscissa,
        ordinates,
        line_predicted,
        line_above,
        line_under,
    )


def get_report(lsm_description: LSMDescription, path_to_save: str = "") -> str:
    """
    Функция для формирования отчета о результатах МНК

    :param: lsm_description - описание МНК
    :param: path_to_save - путь к файлу для сохранения отчета

    :return: строка - отчет определенного формата
    """
    global PRECISION
    # ваш код
    # эту строчку можно менять

    # a = 2
    # n = 3
    # f'{a:.{n}f}'
    # '2.000'

    text = (
        "========================================LSM computing result========="
        "===============================\n"
        "\n"
        f"[INFO]: incline: {lsm_description.incline:.{3}f};\n"
        f"[INFO]: shift: {lsm_description.shift:.{3}f};\n"
        f"[INFO]: incline error: {lsm_description.incline_error:.{3}f};\n"
        f"[INFO]: shift error: {lsm_description.shift_error:.{3}f};\n"
        "\n"
        "=================================================="
        "=================================================="
    )

    if path_to_save != "":
        file = open(path_to_save, "w")
        file.write(text)
        file.close()

    return text


# служебная функция для валидации
def _is_valid_measurments(measurments: list[float]) -> bool:
    # ваш код
    # эту строчку можно менять
    return False


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
        abscissa: list[float],
        ordinates: list[float],
        mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL,
) -> tuple[list[float], list[float]]:
    global event_logger

    # ваш код
    # эту строчку можно менять
    return [], []


# служебная функция для получения статистик
def _get_lsm_statistics(abscissa: list[float], ordinates: list[float]) -> LSMStatistics:
    global event_logger, PRECISION

    # ваш код
    # эту строчку можно менять
    return LSMStatistics(
        abscissa_mean=0, ordinate_mean=0, product_mean=0, abs_squared_mean=0
    )


# служебная функция для получения описания МНК
def _get_lsm_description(
        abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global event_logger, PRECISION

    # ваш код
    # эту строчку можно менять
    return LSMDescription(incline=0, shift=0, incline_error=0, shift_error=0)

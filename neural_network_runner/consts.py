DEFAULT_NETWORK = """
{
    'currentYearEarnings': math.tanh(
        (-0.00010381825268268585 + 0.18721315264701843 * math.tanh((0.07715418934822083 + 0.2497957944869995 * (
                input['ms_komot'] or 0) + 0.09997048228979111 * (input[
                                                                     'gova_simplex_2019'] or 0) + 0.06946669518947601 * (
                                                                            input[
                                                                                'max_height'] or 0) + 0.18702617287635803 * (
                                                                            input[
                                                                                'min_height'] or 0) + 0.13210098445415497 * (
                                                                            input[
                                                                                'lastYearEarnings'] or 0) + 0.0886882022023201 * (
                                                                            input[
                                                                                'neighborhoodName'] or 0))) + 0.021413132548332214 * math.tanh(
            (-0.026864666491746902 + 0.013241570442914963 * (input['ms_komot'] or 0) + 0.08295486122369766 * (
                    input['gova_simplex_2019'] or 0) + 0.0017433672910556197 * (
                     input['max_height'] or 0) + 0.04051709547638893 * (
                     input['min_height'] or 0) + 0.05738107115030289 * (
                     input['lastYearEarnings'] or 0) - 0.10002318024635315 * (
                     input['neighborhoodName'] or 0))) + 0.07428054511547089 * math.tanh((
                -0.12642335891723633 + 0.018793080002069473 * (
                input[
                    'ms_komot'] or 0) - 0.0809822827577591 * (
                        input[
                            'gova_simplex_2019'] or 0) + 0.19228604435920715 * (
                        input[
                            'max_height'] or 0) - 0.1804218739271164 * (
                        input[
                            'min_height'] or 0) + 0.15047234296798706 * (
                        input[
                            'lastYearEarnings'] or 0) - 0.0037414832040667534 * (
                        input[
                            'neighborhoodName'] or 0)))))
}"""

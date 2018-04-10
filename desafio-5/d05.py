# https://osprogramadores.com/desafios/d05/

# http://www.bcampos.com/Graphs.php

import json
import sys

def processar(filename):

    with open(filename) as f:
        dados = json.load(f)

    areas_descr = {x['codigo']: x['nome'] for x in dados['areas']}
    gmaior, gmenor, gsoma, gqtde = None, None, 0, 0
    fmais, fmenos = [], []
    ais = {}  # área info's
    sis = {}  # sobrenome info's

    for func in dados['funcionarios']:
        sob = func['sobrenome']
        sal = func['salario']

        try:
            if sal > gmaior:
                gmaior = sal
                fmais = [func]
            elif sal == gmaior:
                fmais.append(func)
        except:
            gmaior = sal
            fmais.append(func)

        try:
            if sal < gmenor:
                gmenor = sal
                fmenos = [func]
            elif sal == gmenor:
                fmenos.append(func)
        except:
            gmenor = sal
            fmenos.append(func)

        gsoma += sal
        gqtde += 1

        area = func['area']
        try:
            ai = ais[area]
            if sal > ai[0]:
                ai[0] = sal
                ai[4] = [func]
            elif sal == ai[0]:
                ai[4].append(func)

            if sal < ai[1]:
                ai[1] = sal
                ai[5] = [func]
            elif sal == ai[1]:
                ai[5].append(func)

            ai[2] += sal
            ai[3] += 1
        except:
            # maior, menor, soma, qtde, funcs que ganham mais, funcs que ganham menos
            ais[area] = [sal, sal, sal, 1, [func], [func]]

        try:
            si = sis[sob]
            _sal = si[0]
            si[1] += 1
            if sal > _sal:
                si[0] = sal
                si[2] = [func]
            elif sal == _sal:
                si[2].append(func)
        except:
            # maior, qtde, funcs que ganham mais
            sis[sob] = [sal, 1, [func]]

    return(dados['funcionarios'], areas_descr, gmaior, gmenor, gsoma, gqtde, fmais, fmenos, ais, sis)


def gerar_saida(funcs_list, areas_descr, gmaior, gmenor, gsoma, gqtde, fmais, fmenos, ais, sis):
    output = []
    out = output.append

    # QUESTÃO 1

    for func in fmais:
        out('global_max|{} {}|{:.2f}'.format(func['nome'], func['sobrenome'], func['salario']))
    for func in fmenos:
        out('global_min|{} {}|{:.2f}'.format(func['nome'], func['sobrenome'], func['salario']))

    out("global_avg|{media:.2f}".format(media=gsoma / gqtde))


    # # QUESTÃO 2

    for area, (_, _, asoma, aqtde, afuncsmais, afuncsmenos) in ais.items():
        area_descr = areas_descr[area]
        for func in afuncsmais:
            out('area_max|{}|{} {}|{:.2f}'.format(area_descr, func['nome'], func['sobrenome'], func['salario']))
        for func in afuncsmenos:
            out('area_min|{}|{} {}|{:.2f}'.format(area_descr, func['nome'], func['sobrenome'], func['salario']))

        out("area_avg|{a}|{media:.2f}".format(a=area_descr, media=asoma / aqtde))


    # # QUESTÃO 3

    max_area_qtde = max(a[3] for a in ais.values())
    min_area_qtde = min(a[3] for a in ais.values())

    for area, info in ais.items():
        if info[3] == max_area_qtde:
            out("most_employees|{a}|{qtde}".format(a=areas_descr[area], qtde=max_area_qtde))
        if info[3] == min_area_qtde:
            out("least_employees|{a}|{qtde}".format(a=areas_descr[area], qtde=min_area_qtde))


    # # QUESTÃO 4

    for info in sis.values():
        if info[1] > 1:
            for func in info[2]:
                sob = func['sobrenome']
                out('last_name_max|{}|{} {}|{:.2f}'.format(sob, func['nome'], sob, func['salario']))

    print("\n".join(output))



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {}  filename.json'.format(sys.argv[0]))
        sys.exit(2)

    gerar_saida(*processar(sys.argv[1]))

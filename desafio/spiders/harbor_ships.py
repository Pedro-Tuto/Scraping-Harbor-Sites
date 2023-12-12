from pathlib import Path

import scrapy

from desafio.items import Product


class HarborShips(scrapy.Spider):
    name = "harbor_ships"

    def start_requests(self):
        urls = [
            "https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo",
            "https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/",
        ]

        yield scrapy.Request(url=urls[0], callback=self.parse_paranagua)
        yield scrapy.Request(url=urls[1], callback=self.parse_santos)

    def parse_paranagua(self, response):
        table_titles = [
            "ATRACADOS",
            "PROGRAMADOS",
            "AO LARGO PARA REATRACAÇÃO",
            "AO LARGO",
            "ESPERADOS",
            "DESPACHADOS",
        ]
        PORTO = "Paranaguá"

        for title in table_titles:
            table_html = response.xpath(
                f'//table[.//*[text()="{title}"]]'
            ).extract_first()
            table_selector = scrapy.Selector(text=table_html)

            direction_column = (
                'count(//table/thead/tr/th[.=" Sentido"]/preceding-sibling::th)+1'
            )
            expected_column = (
                'count(//table/thead/tr/th[.=" Previsto"]/preceding-sibling::th)+1'
            )
            merchandise_column = 'count(//table/thead/tr/th[contains(text()," Mercadoria")]/preceding-sibling::th)+1'

            table_head_columns = len(
                table_selector.xpath(".//thead/tr[2]/th").extract()
            )
            table_rows = table_selector.xpath(".//tbody/tr")
            for row in table_rows:
                values = row.xpath("./td").extract()

                SKIP_COLUMNS = 0
                if len(values) < table_head_columns:
                    SKIP_COLUMNS = 8

                direction = row.xpath(
                    f"./td[{direction_column}-{SKIP_COLUMNS}]/text()"
                ).extract_first()
                expected_volume = row.xpath(
                    f"./td[{expected_column}-{SKIP_COLUMNS}]/text()"
                ).extract_first()
                merchandise = row.xpath(
                    f"./td[{merchandise_column}-{SKIP_COLUMNS}]/text()"
                ).extract_first()

                volume = expected_volume.split()
                is_in_tons = volume[1] == "Tons."

                product = Product(
                    harbor=PORTO,
                    merchandise=merchandise,
                    direction=direction,
                    daily_volume_in_tons=volume[0] if is_in_tons else None,
                    daily_volume_in_movs=volume[0] if not is_in_tons else None,
                )

                yield product

    def parse_santos(self, response):
        table_titles = [
            "LIQUIDO A GRANEL",
            "TRIGO",
            "GRANEIS DE ORIGEM VEGETAL",
            "GRANEIS SOLIDOS - IMPORTACAO",
            "GRANEIS SOLIDOS - EXPORTACAO",
            "ROLL-IN-ROLL-OFF",
            "LASH",
            "CABOTAGEM",
            "CONTEINERES",
            "PRIORIDADE C5",
            "SEM PRIORIDADE",
        ]
        PORTO = "Santos"

        for title in table_titles:
            table_html = response.xpath(
                f'//table[.//*[text()="{title}"]]'
            ).extract_first()
            table_selector = scrapy.Selector(text=table_html)

            direction_column = 'count(//table/thead/tr/th[contains(text(),"Operaç")]/preceding-sibling::th)+1'
            expected_column = 'count(//table/thead/tr/th[contains(text(),"Peso")]/preceding-sibling::th)+1'
            merchandise_column = 'count(//table/thead/tr/th[contains(text(),"Mercadoria")]/preceding-sibling::th)+1'

            rows = table_selector.xpath(".//tbody/tr")

            for row in rows:
                direction = ", ".join(
                    row.xpath(f".//td[{direction_column}]/text()").extract()
                )
                expected_volume = ", ".join(
                    row.xpath(f".//td[{expected_column}]/text()").extract()
                )
                merchandise = ", ".join(
                    row.xpath(f".//td[{merchandise_column}]/text()").extract()
                )

                product = Product(
                    harbor=PORTO,
                    merchandise=merchandise,
                    direction=direction,
                    daily_volume_in_tons=expected_volume,
                    daily_volume_in_movs=None,
                )

                yield product

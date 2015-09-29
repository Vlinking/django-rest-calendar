# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendaruser',
            name='timezone',
            field=models.CharField(default=b'Europe/Warsaw', max_length=50, choices=[(b'Europe/Amsterdam', b'Europe/Amsterdam'), (b'Europe/Andorra', b'Europe/Andorra'), (b'Europe/Athens', b'Europe/Athens'), (b'Europe/Belfast', b'Europe/Belfast'), (b'Europe/Belgrade', b'Europe/Belgrade'), (b'Europe/Berlin', b'Europe/Berlin'), (b'Europe/Bratislava', b'Europe/Bratislava'), (b'Europe/Brussels', b'Europe/Brussels'), (b'Europe/Bucharest', b'Europe/Bucharest'), (b'Europe/Budapest', b'Europe/Budapest'), (b'Europe/Busingen', b'Europe/Busingen'), (b'Europe/Chisinau', b'Europe/Chisinau'), (b'Europe/Copenhagen', b'Europe/Copenhagen'), (b'Europe/Dublin', b'Europe/Dublin'), (b'Europe/Gibraltar', b'Europe/Gibraltar'), (b'Europe/Guernsey', b'Europe/Guernsey'), (b'Europe/Helsinki', b'Europe/Helsinki'), (b'Europe/Isle_of_Man', b'Europe/Isle_of_Man'), (b'Europe/Istanbul', b'Europe/Istanbul'), (b'Europe/Jersey', b'Europe/Jersey'), (b'Europe/Kaliningrad', b'Europe/Kaliningrad'), (b'Europe/Kiev', b'Europe/Kiev'), (b'Europe/Lisbon', b'Europe/Lisbon'), (b'Europe/Ljubljana', b'Europe/Ljubljana'), (b'Europe/London', b'Europe/London'), (b'Europe/Luxembourg', b'Europe/Luxembourg'), (b'Europe/Madrid', b'Europe/Madrid'), (b'Europe/Malta', b'Europe/Malta'), (b'Europe/Mariehamn', b'Europe/Mariehamn'), (b'Europe/Minsk', b'Europe/Minsk'), (b'Europe/Monaco', b'Europe/Monaco'), (b'Europe/Moscow', b'Europe/Moscow'), (b'Europe/Nicosia', b'Europe/Nicosia'), (b'Europe/Oslo', b'Europe/Oslo'), (b'Europe/Paris', b'Europe/Paris'), (b'Europe/Podgorica', b'Europe/Podgorica'), (b'Europe/Prague', b'Europe/Prague'), (b'Europe/Riga', b'Europe/Riga'), (b'Europe/Rome', b'Europe/Rome'), (b'Europe/Samara', b'Europe/Samara'), (b'Europe/San_Marino', b'Europe/San_Marino'), (b'Europe/Sarajevo', b'Europe/Sarajevo'), (b'Europe/Simferopol', b'Europe/Simferopol'), (b'Europe/Skopje', b'Europe/Skopje'), (b'Europe/Sofia', b'Europe/Sofia'), (b'Europe/Stockholm', b'Europe/Stockholm'), (b'Europe/Tallinn', b'Europe/Tallinn'), (b'Europe/Tirane', b'Europe/Tirane'), (b'Europe/Tiraspol', b'Europe/Tiraspol'), (b'Europe/Uzhgorod', b'Europe/Uzhgorod'), (b'Europe/Vaduz', b'Europe/Vaduz'), (b'Europe/Vatican', b'Europe/Vatican'), (b'Europe/Vienna', b'Europe/Vienna'), (b'Europe/Vilnius', b'Europe/Vilnius'), (b'Europe/Volgograd', b'Europe/Volgograd'), (b'Europe/Warsaw', b'Europe/Warsaw'), (b'Europe/Zagreb', b'Europe/Zagreb'), (b'Europe/Zaporozhye', b'Europe/Zaporozhye'), (b'Europe/Zurich', b'Europe/Zurich')]),
        ),
    ]

class NotifyChannels:
    """Core NotifyMSTeam Class.
    Usage:
    from NotifyChannels import webhook
    Send Messages to webhook url"""

    webhook = {
        "dba-test-notifications": {
            "uri": "https://prod-157.westus.logic.azure.com:443/workflows/599550925b284cbbaef293a1b230f83e/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=kW5rtNSU5k0QjUarG8U3p3DGTe_0tfil9x4BMJyRjU4"
        },
        "dba": {
            "uri": "https://prod-177.westus.logic.azure.com:443/workflows/7da4b651258a4b4fb23ab21f9b05f172/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Eka0XTjDPjV0bMBHaVhZFkXKp5gK9_kdShSNpCBi4UQ"
        },
        "dba-only": {
            "uri": "https://prod-49.westus.logic.azure.com:443/workflows/eb0ab4c596fe489d9979ff50757ec328/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=fuVWJIofNne_cL5xc0PBxRium70F1KyjQ98bRHGJsKY"
        },
        "costar-dba-team-general": {
            "uri": "https://prod-51.westus.logic.azure.com:443/workflows/1e389306783e4aea9eee10a0b4e750de/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=grrNrULQP7WpPeq4WSK-3ZezN7iQQFf4RATNWCZs-vw"
        },
        "costar-dba-arch-grp": {
            "uri": "https://prod-27.westus.logic.azure.com:443/workflows/2acaf56611ad4b36a0ca65c61d3dfc93/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=LVccpRroSXn7lO_9BhsLu4iRykdOlo2AbR39cdW_GCY"
        },
        "dba-ec2-automation-alert": {
            "uri": "https://prod-32.westus.logic.azure.com:443/workflows/094704310e8b42108d7d1d3b052e1d1f/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=O5n5VbGzaVvuYrqUneJFPcz1x_fXHp72biZiMJm74Jc"
        },
        "dba-general": {
            "uri": "https://prod-181.westus.logic.azure.com:443/workflows/592f1b1b1de74b2e9eeb753a87a9a5b7/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=tXhDjRuuxM9bPuut9ii3gYTGllWB9WLUsZXbbzOXwOA"
        },
        # "dba-general-alert": {
        #     "uri": "https://prod-175.westus.logic.azure.com:443/workflows/66f913e7977f4b3cbc833a8f5d3b3bb8/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=GZY5lkL_787Fba78BiSA_3szRrwc5een1LeDV6-F0oM"
        #     # "https://costarsoftware.webhook.office.com/webhookb2/b923c9ac-b5ca-4ed7-840b-a6d5e164b5c9@9a64e7ca-363f-441c-9aa7-4f85977c09f1/IncomingWebhook/dbf0ed632c2b49c983ac4b65f0dac1f1/81daef56-1264-4126-99c5-f4b2b77a813c/0001xoJjXHzAjhKo3Nt4rBU-jN5EWLzzoORsknkgX4BSqnc1"
        # },
        "aws-sbx-cleanup-alerts-stacklet": {
            "uri": "https://prod-121.westus.logic.azure.com:443/workflows/b15e81b35d9d49f391d195d7ce5053fd/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=vycH3XKhAy2axmsAM6X7moyNkisHzjN-nwsgjI4Jxvk"
        },
        "aws-sbx-cleanup-alerts-report": {
            "uri": "https://prod-01.westus.logic.azure.com:443/workflows/3558daa208964f0188298ef052634210/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=mOdThie9NzcUbr5x9MNx1BTD6V8VuY0mMXVvzXU__Ws"
        },
        "dba-atlas-prd-alerts": {
            "uri": "https://prod-142.westus.logic.azure.com:443/workflows/5c43c85648b34c0186d9ae846e82fdc8/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=p1XlEckbiaxpolwxH0MpQ3SyGO1vSv-YZXDG4My3MTo"
        },
        "dba-cluster-failovers": {
            "uri": "https://prod-126.westus.logic.azure.com:443/workflows/bb9a040b42ff4821a42ab9f1e2a3dae1/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=EHKaXH5eEkV4u9sYSvDW5Lda8qH2CcfcK00BGcYRh1o"
        },
        "dba-ec2-cattle-alerts": {
            "uri": "https://prod-191.westus.logic.azure.com:443/workflows/c2ce5b1ec8994fb7bdea06ce58f6788e/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=9QLXip00jtllllt8PBDWIHTofSoUDDMUdwhXnxDUans"
        },
        "dba-mapinfo-dev-alert": {
            "uri": "https://prod-136.westus.logic.azure.com:443/workflows/bb5f4b19dad947f2b9f09269102ab4d8/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=hKUAa2mb5YF3HIWdvXKLeJi1UUydfkP8vHZrUYdYdh0"
        },
        "dba-mapinfo-prd-alert": {
            "uri": "https://prod-19.westus.logic.azure.com:443/workflows/d38bff2bd5554cf2a954473daafb375b/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=H3RXO-i07QxLaX7iEXj9obFCzZnqpxKnIWq1pcR8QVk"
        },
        "dba-mapinfo-tst-alert": {
            "uri": "https://prod-135.westus.logic.azure.com:443/workflows/1d30e9f07e9d4b589d6a4b038ac44639/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=em_awrqPm2FsgvmixM3KGPU5yHYsmGxQMS8rgtnpNig"
        },
        "dba-rds-dev-alerts": {
            "uri": "https://prod-113.westus.logic.azure.com:443/workflows/ab87c2d4ecfd4f2bb12a4793dc0617f9/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=omHPPSAehDLcLk2oHQ-1Ba3rMTRM8UNQAeN602Oo2rQ"
        },
        "dba-rds-tst-alerts": {
            "uri": "https://prod-191.westus.logic.azure.com:443/workflows/8dc98b4d12eb49b180bdf658e5d1dbd6/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=8sdR32nUAcutebhxCiFkiup0h7N_hYcGQkMc7oE0yK4"
        },
        "dba-rds-prd-alerts": {
            "uri": "https://prod-89.westus.logic.azure.com:443/workflows/9b5f6462844f4dc6926adcb4c8cc9a63/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=oH--NPdT1iHck0fhl6XYwhdlTBi5HAVHQEf654k-aOI"
        },
        "dba-research-prd-alerts": {
            "uri": "https://prod-117.westus.logic.azure.com:443/workflows/b2be6d3cfbfc48928c67837e11ee2fc4/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=-V5NzL8TjlEJbKkueJmRY0UBYMKbQdLHZ_btSS0sFq8"
        },
        "dba-snowflake-notifications": {
            "uri": "https://prod-156.westus.logic.azure.com:443/workflows/17fe8444f27b41a1a37a361fa0e54078/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=aYGnULglw5SJkKozwznuWZstp5N1ZtBs6tadsJ0oYtE"
        },
        "dba-snowflake-notifications-dev-tst": {
            "uri": "https://prod-89.westus.logic.azure.com:443/workflows/5e2281e9a4e748f18fd5557512b6afdf/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=3MFx03ne7-ky4ivb4Hhx39RNJW7XIrV4lzRv_fZalm0"
        },
        "homes-analytics-alerts": {
            "uri": "https://prod-141.westus.logic.azure.com:443/workflows/8321305344d14d32bf41d15d0d57c827/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=MAn0QQhwloouGqJRa_Kr0qE9WAYGGRkEnuPJ9y6oaYI"
        }
    }

    def __init__(self, channel: str) -> str:
        self.webhook = self.webhook["channel"]["uri"]
        return self.webhook

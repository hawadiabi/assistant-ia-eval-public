import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(
    command=sys.executable,
    args=[str(Path(__file__).parent / "serveur_mcp.py")],
)


async def appeler(session, outil, arguments):
    resultat = await session.call_tool(outil, arguments)
    print(f"--- {outil} {arguments}")
    print(resultat.content[0].text)


async def main():
    async with stdio_client(params) as (lecture, ecriture):
        async with ClientSession(lecture, ecriture) as session:
            await session.initialize()
            outils = await session.list_tools()
            print("Outils disponibles :", [o.name for o in outils.tools])
            await appeler(session, "chercher_verbe", {"verbe": "aller"})
            await appeler(session, "lire_fichier", {"nom": "imparfait.md"})
            await appeler(
                session,
                "envoyer_courriel",
                {"destinataire": "test@example.com", "sujet": "Test", "corps": "Bonjour"},
            )


asyncio.run(main())
# flake8: noqa: E501
import httpx
import asyncio
from app.config import settings
from app.exceptions import RiotAPIError


class RiotClient:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(15))
        self.headers = {"X-Riot-Token": settings.API_RIOT_KEY}
        self.semaphore = asyncio.Semaphore(10)

    async def close(self):
        await self.client.aclose()

    async def _request(self, url: str, retries: int = 3):
        async with self.semaphore:
            for attempt in range(retries):
                response = await self.client.get(url, headers=self.headers)

                if response.status_code == 200:
                    return response.json()

                if response.status_code == 404:
                    return None

                if response.status_code == 403:
                    raise RiotAPIError("Riot API key expired or invalid")

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", "1"))
                    await asyncio.sleep(retry_after)
                    continue

                if response.status_code >= 500:
                    await asyncio.sleep(2**attempt)
                    continue

                response.raise_for_status()

            raise RiotAPIError(
                f"Riot API request failed after {retries} retries: {url}"
            )

    async def get_account_by_riot_id(
        self, game_name: str, tag_line: str, regional_host: str = "europe"
    ):
        url = f"https://{regional_host}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return await self._request(url)

    async def get_summoner_by_puuid(self, puuid: str, platform_host: str = "euw1"):
        url = f"https://{platform_host}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        return await self._request(url)

    async def get_ranked_entries(self, puuid: str, platform_host="euw1"):
        url = f"https://{platform_host}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
        return await self._request(url)

    async def get_match_ids(
        self, puuid: str, count: int = 20, regional_host: str = "europe"
    ):
        url = f"https://{regional_host}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
        return await self._request(url)

    async def get_match(self, match_id: str, regional_host: str = "europe"):
        url = (
            f"https://{regional_host}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        )
        return await self._request(url)

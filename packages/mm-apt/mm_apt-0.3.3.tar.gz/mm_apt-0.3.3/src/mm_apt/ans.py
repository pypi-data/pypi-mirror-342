from mm_std import Result, http_request


async def address_to_name(address: str, timeout: float = 5, proxy: str | None = None) -> Result[str | None]:
    url = f"https://www.aptosnames.com/api/mainnet/v1/name/{address}"
    res = await http_request(url, proxy=proxy, timeout=timeout)
    if res.is_err():
        return res.to_err()
    json_res = res.parse_json_body()
    if res.status_code == 200 and json_res == {}:
        return res.to_ok(None)
    if "name" in json_res:
        return res.to_ok(json_res["name"])
    return res.to_err("unknown_response")


async def address_to_primary_name(address: str, timeout: float = 5, proxy: str | None = None) -> Result[str | None]:
    url = f"https://www.aptosnames.com/api/mainnet/v1/primary-name/{address}"
    res = await http_request(url, proxy=proxy, timeout=timeout)
    if res.is_err():
        return res.to_err()
    json_res = res.parse_json_body()
    if res.status_code == 200 and json_res == {}:
        return res.to_ok(None)
    if "name" in json_res:
        return res.to_ok(json_res["name"])
    return res.to_err("unknown_response")

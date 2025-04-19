from mm_std import Result, http_request


async def address_to_name(address: str, timeout: float = 5, proxy: str | None = None) -> Result[str | None]:
    url = f"https://www.aptosnames.com/api/mainnet/v1/name/{address}"
    res = await http_request(url, proxy=proxy, timeout=timeout)
    if res.is_err():
        return res.to_err_result()
    json_res = res.parse_json_body()
    if res.status_code == 200 and json_res == {}:
        return res.to_ok_result(None)
    if "name" in json_res:
        return res.to_ok_result(json_res["name"])
    return res.to_err_result("unknown_response")


async def address_to_primary_name(address: str, timeout: float = 5, proxy: str | None = None) -> Result[str | None]:
    url = f"https://www.aptosnames.com/api/mainnet/v1/primary-name/{address}"
    res = await http_request(url, proxy=proxy, timeout=timeout)
    if res.is_err():
        return res.to_err_result()
    json_res = res.parse_json_body()
    if res.status_code == 200 and json_res == {}:
        return res.to_ok_result(None)
    if "name" in json_res:
        return res.to_ok_result(json_res["name"])
    return res.to_err_result("unknown_response")

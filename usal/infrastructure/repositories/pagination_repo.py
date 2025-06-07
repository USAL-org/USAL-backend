from math import ceil

from usal.domain.entities.common_entity import PageEntity


async def paginate(total_records: int, page: int, limit: int) -> PageEntity:
    if total_records == 0:
        return PageEntity(
            total_pages=0,
            total_records=0,
            next=None,
            previous=None,
            record_range=[0, 0],
            current_page=0,
            offset=0,
        )

    total_pages = ceil(total_records / limit)
    offset = (page - 1) * limit if total_pages else 0

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    return PageEntity(
        total_pages=total_pages,
        total_records=total_records,
        next=f"/?page={page + 1}" if page < total_pages else None,
        previous=f"/?page={page - 1}" if page > 1 else None,
        record_range=[offset + 1, min(offset + limit, total_records)],
        current_page=page,
        offset=offset,
    )

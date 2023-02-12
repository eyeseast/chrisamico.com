select
    *
from
    links
    left join mastodon on links.id = mastodon.link_id
where
    (
        mastodon.status is null
        or mastodon.status = 'failed'
    )
    and datetime(published) >= datetime('now', '-24 hours')
order by
    published desc
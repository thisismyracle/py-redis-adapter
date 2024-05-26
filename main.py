""" The main file to test the basic case of using Cache module """

from cache import Cache


if __name__ == '__main__':

    # Create cache connection
    cache = Cache('my_cache', '127.0.0.1', 6379)
    cache.setup_passphrase('lorem-ipsum')

    # Check if sub exists
    print('Is users exists?')
    is_exists = cache.is_sub_exists('users')  # pylint: disable=C0103
    print(is_exists)

    # ADMINISTRATIVE: Delete the sub if exists
    if is_exists:
        print('\nDeleting sub if exists')
        print(cache.delete_sub('users', passphrase='lorem-ipsum'))

    # ADMINISTRATIVE: Create new table
    print('\nCreate new sub called users')
    print(cache.create_sub('users', {
        'uid': 'INTEGER',
        'name': 'TEXT',
        'status': 'BOOLEAN'
    }, passphrase='lorem-ipsum'))

    # TIPS: Always include passphrase in function args to perform administrative task
    #       such as create_table and delete_table.
    #       This passphrase is not secret, but is always needed to perform administrative task.

    # Check if table exists (again)
    print('\nIs users exists? (2)')
    print(cache.is_sub_exists('users'))

    # GET-ALL statement
    print('\nLets see the users contains')
    print(cache.sub('users').get_all())

    # SET statement
    print('\nLets set an user')
    print(cache.sub('users').set(800099, {
        'name': 'Alex',
        'status': True
    }))
    print(cache.sub('users').get_all())

    # SET-MANY statement
    print('\nLets set more users in bulk!')
    print(cache.sub('users').set_many({
        800100: {
            'name': 'Becky',
            'status': False
        },
        800209: {
            'name': 'Cockney',
            'status': True
        },
        803333: {
            'name': 'Doodle',
            'status': True
        }
    }))
    print(cache.sub('users').get_all())

    # GET-MANY statement
    print('\nHow about we get some users??')
    print(cache.sub('users').get_many([
        800099, 800209
    ]))

    # GET statement
    print('\nLet\'s be real, get one cache only.')
    print(cache.sub('users').get(800100))

    # GET statement (but actually the cache don't have it)
    print('\nWhat if the cache do not have it?')
    print(cache.sub('users').get(999999))

    # GET-MANY statement (but actually the cache just have a part of it)
    print('\nWhat if the cache just have a part? (2)')
    print(cache.sub('users').get_many([
        100000, 800209
    ]))

    # UNSET statement
    print('\nI wanna end this specified man session >:)')
    print(cache.sub('users').get_all())
    print(cache.sub('users').unset(800099))
    print(cache.sub('users').get_all())

    # UNSET-MANY statement
    print('\nI don\'t like these guyssss >:)')
    print(cache.sub('users').get_all())
    print(cache.sub('users').unset_many([800209, 800100]))
    print(cache.sub('users').get_all())

    # UNSET-ALL statement
    print('\nLet\'s go add more and flush them all!!!')
    print(cache.sub('users').set_many({
        800100: {
            'name': 'Eerie',
            'status': False
        },
        800209: {
            'name': 'Fellman',
            'status': False
        },
        803333: {
            'name': 'Gooliver',
            'status': True
        }
    }))
    print(cache.sub('users').get_all())
    print(cache.sub('users').unset_all())
    print(cache.sub('users').get_all())


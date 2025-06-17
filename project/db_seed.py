from apps.posts.models import Post, Category
from apps.users.models import User
from apps.posts.automated_fetcher.main_reader import MainReader
import random

def seed_users():
    User.objects.get_or_create(
        email='test@test.com',
        defaults={
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )

def seed_categories():
    categories = [
        {
            'name': 'General',
            'description': 'General posts about various topics'
        },
        {
            'name': 'History',
            'description': 'Posts about historical events and figures'
        },
        {
            'name': 'Entertainment',
            'description': 'Posts about movies, music, and entertainment'
        }
    ]

    for category_data in categories:
        Category.objects.get_or_create(
            name=category_data['name'],
            defaults={'description': category_data['description']}
        )

def seed_posts():
    user = User.objects.first()  # Assuming the user is already seeded
    if not user:
        seed_users()
        user = User.objects.first()

    links = ['https://www.youtube.com/watch?v=tZi4fDXG_N0', 'https://www.youtube.com/watch?v=UjXvq_YyeZ0', 'https://www.youtube.com/watch?v=mNDYNQ80gLY', 'https://www.youtube.com/watch?v=x3UFAooTy2M', 'https://www.youtube.com/watch?v=VYUZJ7ykmRM', 'https://www.youtube.com/watch?v=l627VqCmfIA', 'https://www.youtube.com/watch?v=Zb2LmS1TkvI', 'https://www.youtube.com/watch?v=hVYE0diIBI4', 'https://www.youtube.com/watch?v=sV-b64qrDK8', 'https://www.youtube.com/watch?v=wOob88YwTFA', 'https://www.youtube.com/watch?v=fM6meqsQpX4', 'https://www.youtube.com/watch?v=8RkNANMKY-k', 'https://www.youtube.com/watch?v=0BFHcb0oyiM', 'https://www.youtube.com/watch?v=FfuAw0601cE', 'https://www.youtube.com/watch?v=udrcf15LyhI', 'https://www.youtube.com/watch?v=K8gZYfkJVfw', 'https://www.youtube.com/watch?v=c4zx1qyZiWc', 'https://www.youtube.com/watch?v=8KNLPYqPzUY', 'https://www.youtube.com/watch?v=zlMQnRFLEMc', 'https://www.youtube.com/watch?v=qK7lV0tMAGo', 'https://www.youtube.com/watch?v=ZdAjA7x-I9E', 'https://www.youtube.com/watch?v=flRo2I7D24Y', 'https://www.youtube.com/watch?v=YAl4PWSihTc', 'https://www.youtube.com/watch?v=K6sbb2RKaus', 'https://www.youtube.com/watch?v=3TVrqPXtq24', 'https://www.youtube.com/watch?v=632QwUbhL04', 'https://www.youtube.com/watch?v=pBHZPJC2oFY', 'https://www.youtube.com/watch?v=mMzOcNqoXo8', 'https://www.youtube.com/watch?v=pRAi708jknA', 'https://www.youtube.com/watch?v=OMOuz4fmvL0']

    for link in links:
        try:
            reader = MainReader(link)
            video_info = reader.read()

            # Get all categories and randomly select 2
            all_categories = list(Category.objects.all())
            random_categories = random.sample(all_categories, min(2, len(all_categories)))

            # First create or get the post
            post, created = Post.objects.get_or_create(
                title=video_info['title'],
                defaults={
                    'description': video_info['description'],
                    'duration': video_info['duration'],
                    'link': link,
                    'user': user,
                    'publish_date': video_info.get('publish_date', None),
                }
            )

            # Then set the categories
            if created:
                post.categories.set(random_categories)
                print(f"Created post: {post.title} with categories: {[c.name for c in random_categories]}")
            else:
                print(f"Post already exists: {post.title}")

        except Exception as e:
            print(f"Error processing link {link}: {str(e)}")
            continue

def run_seed():
    print('Seeding users...')
    seed_users()
    print('Seeding categories...')
    seed_categories()
    print('Seeding posts...')
    seed_posts()
    print('Seeding completed!')

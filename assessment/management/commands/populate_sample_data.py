from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from assessment.models import Questionnaire, Question, QuestionOption, AssessmentResult
from resources.models import ResourceCategory, Resource, GuidanceContent, CrisisResource, FAQ

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample questionnaire
        questionnaire, created = Questionnaire.objects.get_or_create(
            name="Mental Health Self-Assessment",
            defaults={
                'description': 'A comprehensive assessment to evaluate your mental health status across multiple dimensions.',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created questionnaire: {questionnaire.name}')
        
        # Create sample questions
        questions_data = [
            {
                'text': 'How would you rate your overall mood over the past week?',
                'question_type': 'single_choice',
                'order': 1,
                'options': [
                    ('Very poor', 1),
                    ('Poor', 2),
                    ('Fair', 3),
                    ('Good', 4),
                    ('Excellent', 5)
                ]
            },
            {
                'text': 'How has your sleep quality been recently?',
                'question_type': 'single_choice',
                'order': 2,
                'options': [
                    ('Very poor', 1),
                    ('Poor', 2),
                    ('Fair', 3),
                    ('Good', 4),
                    ('Excellent', 5)
                ]
            },
            {
                'text': 'How would you describe your current stress level?',
                'question_type': 'single_choice',
                'order': 3,
                'options': [
                    ('Very high', 1),
                    ('High', 2),
                    ('Moderate', 3),
                    ('Low', 4),
                    ('Very low', 5)
                ]
            },
            {
                'text': 'How connected do you feel to others?',
                'question_type': 'single_choice',
                'order': 4,
                'options': [
                    ('Very isolated', 1),
                    ('Somewhat isolated', 2),
                    ('Neutral', 3),
                    ('Somewhat connected', 4),
                    ('Very connected', 5)
                ]
            },
            {
                'text': 'How would you rate your energy level?',
                'question_type': 'single_choice',
                'order': 5,
                'options': [
                    ('Very low', 1),
                    ('Low', 2),
                    ('Moderate', 3),
                    ('High', 4),
                    ('Very high', 5)
                ]
            }
        ]
        
        for q_data in questions_data:
            question, created = Question.objects.get_or_create(
                questionnaire=questionnaire,
                text=q_data['text'],
                defaults={
                    'question_type': q_data['question_type'],
                    'order': q_data['order'],
                    'is_required': True
                }
            )
            
            if created:
                self.stdout.write(f'Created question: {question.text[:50]}...')
                
                # Create options for this question
                for option_text, option_value in q_data['options']:
                    QuestionOption.objects.create(
                        question=question,
                        text=option_text,
                        value=option_value
                    )
        
        # Create assessment results
        results_data = [
            {
                'risk_level': 'low',
                'title': 'You\'re doing well!',
                'description': 'Your responses suggest you\'re managing your mental health well.',
                'recommendations': 'Continue your current self-care practices and maintain regular check-ins.',
                'resources': 'Mindfulness apps, exercise routines, social activities',
                'min_score': 0,
                'max_score': 12
            },
            {
                'risk_level': 'moderate',
                'title': 'Some areas for improvement',
                'description': 'Your responses suggest there are some areas where you could benefit from additional support.',
                'recommendations': 'Consider speaking with a mental health professional and practice stress management techniques.',
                'resources': 'Stress management resources, support groups, professional counseling',
                'min_score': 13,
                'max_score': 18
            },
            {
                'risk_level': 'high',
                'title': 'Professional support recommended',
                'description': 'Your responses suggest you may benefit from professional mental health support.',
                'recommendations': 'Please consider reaching out for help from a mental health professional immediately.',
                'resources': 'Crisis helplines, emergency mental health services, professional therapy',
                'min_score': 19,
                'max_score': 25
            }
        ]
        
        for result_data in results_data:
            AssessmentResult.objects.get_or_create(
                risk_level=result_data['risk_level'],
                defaults=result_data
            )
        
        # Create resource categories
        categories_data = [
            {'name': 'Self-Care', 'description': 'Resources for daily self-care practices', 'color': '#10B981'},
            {'name': 'Crisis Support', 'description': 'Emergency and crisis support resources', 'color': '#EF4444'},
            {'name': 'Professional Help', 'description': 'Finding and accessing professional mental health services', 'color': '#3B82F6'},
            {'name': 'Education', 'description': 'Educational materials about mental health', 'color': '#8B5CF6'},
        ]
        
        for cat_data in categories_data:
            ResourceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
        
        # Create sample resources - 10 for each resource type
        resources_data = [
            # ARTICLES (10)
            {'title': 'Understanding Depression: A Comprehensive Guide', 'description': 'Learn about depression symptoms, causes, and effective treatment options from medical experts.', 'resource_type': 'article', 'url': 'https://example.com/depression-guide', 'is_free': True},
            {'title': 'Anxiety Management Techniques You Can Use Today', 'description': 'Practical strategies and techniques to manage anxiety symptoms and improve your daily life.', 'resource_type': 'article', 'url': 'https://example.com/anxiety-management', 'is_free': True},
            {'title': 'Building Resilience: How to Bounce Back from Stress', 'description': 'Evidence-based approaches to building mental resilience and coping with life challenges.', 'resource_type': 'article', 'url': 'https://example.com/resilience', 'is_free': True},
            {'title': 'The Science of Sleep and Mental Health', 'description': 'Discover how quality sleep impacts your mental wellbeing and learn strategies for better rest.', 'resource_type': 'article', 'url': 'https://example.com/sleep-mental-health', 'is_free': True},
            {'title': 'Mindfulness and Meditation: Getting Started Guide', 'description': 'A beginner-friendly guide to starting your mindfulness and meditation practice.', 'resource_type': 'article', 'url': 'https://example.com/mindfulness-guide', 'is_free': True},
            {'title': 'Understanding PTSD: Symptoms and Recovery', 'description': 'Comprehensive information about post-traumatic stress disorder and pathways to healing.', 'resource_type': 'article', 'url': 'https://example.com/ptsd-guide', 'is_free': True},
            {'title': 'Managing Work-Related Stress and Burnout', 'description': 'Practical tips for identifying and managing workplace stress before it leads to burnout.', 'resource_type': 'article', 'url': 'https://example.com/workplace-stress', 'is_free': True},
            {'title': 'Social Anxiety: Understanding and Overcoming', 'description': 'Learn about social anxiety disorder and evidence-based strategies for managing social situations.', 'resource_type': 'article', 'url': 'https://example.com/social-anxiety', 'is_free': True},
            {'title': 'The Connection Between Physical and Mental Health', 'description': 'Explore how exercise, nutrition, and physical wellness impact your mental health.', 'resource_type': 'article', 'url': 'https://example.com/physical-mental-health', 'is_free': True},
            {'title': 'Cognitive Behavioral Therapy (CBT) Explained', 'description': 'Understanding how CBT works and why it\'s effective for treating various mental health conditions.', 'resource_type': 'article', 'url': 'https://example.com/cbt-explained', 'is_free': True},
            
            # VIDEOS (10)
            {'title': '10-Minute Guided Meditation for Stress Relief', 'description': 'A calming guided meditation session designed to reduce stress and promote relaxation.', 'resource_type': 'video', 'url': 'https://example.com/meditation-video', 'is_free': True},
            {'title': 'Understanding Anxiety: Educational Video Series', 'description': 'Comprehensive video series explaining anxiety disorders, their causes, and treatment options.', 'resource_type': 'video', 'url': 'https://example.com/anxiety-videos', 'is_free': True},
            {'title': 'Yoga for Mental Wellness: Beginner Session', 'description': 'Gentle yoga practice specifically designed to support mental health and emotional balance.', 'resource_type': 'video', 'url': 'https://example.com/yoga-mental-health', 'is_free': True},
            {'title': 'Breathing Exercises for Panic Attacks', 'description': 'Learn breathing techniques that can help during panic attacks and moments of high anxiety.', 'resource_type': 'video', 'url': 'https://example.com/breathing-exercises', 'is_free': True},
            {'title': 'Therapy Types Explained: Which is Right for You?', 'description': 'Educational video explaining different types of therapy and how to choose the right approach.', 'resource_type': 'video', 'url': 'https://example.com/therapy-types', 'is_free': True},
            {'title': 'Building Healthy Relationships and Boundaries', 'description': 'Video guide on establishing healthy boundaries and improving relationship dynamics.', 'resource_type': 'video', 'url': 'https://example.com/relationships', 'is_free': True},
            {'title': 'Overcoming Depression: Personal Stories and Strategies', 'description': 'Inspirational video featuring personal recovery stories and practical strategies.', 'resource_type': 'video', 'url': 'https://example.com/depression-stories', 'is_free': True},
            {'title': 'Mindfulness-Based Stress Reduction (MBSR) Introduction', 'description': 'Introduction to MBSR program and its benefits for stress and mental health.', 'resource_type': 'video', 'url': 'https://example.com/mbsr-intro', 'is_free': True},
            {'title': 'Sleep Hygiene: Tips for Better Sleep', 'description': 'Video guide on improving sleep quality through better sleep hygiene practices.', 'resource_type': 'video', 'url': 'https://example.com/sleep-hygiene', 'is_free': True},
            {'title': 'Trauma and Recovery: Understanding the Healing Process', 'description': 'Educational video about trauma, its effects, and the journey toward recovery.', 'resource_type': 'video', 'url': 'https://example.com/trauma-recovery', 'is_free': True},
            
            # PODCASTS (10)
            {'title': 'The Mental Health Podcast: Weekly Discussions', 'description': 'Weekly podcast featuring conversations about mental health, wellness, and personal growth.', 'resource_type': 'podcast', 'url': 'https://example.com/mental-health-podcast', 'is_free': True},
            {'title': 'Anxiety Slayer: Practical Coping Strategies', 'description': 'Podcast dedicated to providing practical tools and strategies for managing anxiety.', 'resource_type': 'podcast', 'url': 'https://example.com/anxiety-slayer', 'is_free': True},
            {'title': 'The Happiness Lab: Science of Wellbeing', 'description': 'Evidence-based podcast exploring the science behind happiness and mental wellbeing.', 'resource_type': 'podcast', 'url': 'https://example.com/happiness-lab', 'is_free': True},
            {'title': 'Depression Stories: Real People, Real Recovery', 'description': 'Podcast featuring real stories of people who have overcome depression and found hope.', 'resource_type': 'podcast', 'url': 'https://example.com/depression-stories-podcast', 'is_free': True},
            {'title': 'Therapy Thoughts: Mental Health Made Simple', 'description': 'Podcast breaking down mental health concepts and therapy approaches in simple terms.', 'resource_type': 'podcast', 'url': 'https://example.com/therapy-thoughts', 'is_free': True},
            {'title': 'Mindful Moments: Daily Meditation Guidance', 'description': 'Daily short meditation and mindfulness podcast episodes for daily practice.', 'resource_type': 'podcast', 'url': 'https://example.com/mindful-moments', 'is_free': True},
            {'title': 'Trauma Talks: Understanding and Healing', 'description': 'Podcast exploring trauma, its impacts, and pathways to healing and recovery.', 'resource_type': 'podcast', 'url': 'https://example.com/trauma-talks', 'is_free': True},
            {'title': 'The Stress Less Podcast', 'description': 'Weekly episodes on managing stress, preventing burnout, and living a balanced life.', 'resource_type': 'podcast', 'url': 'https://example.com/stress-less', 'is_free': True},
            {'title': 'Relationship Therapy: Improving Connections', 'description': 'Podcast about building healthier relationships and improving communication skills.', 'resource_type': 'podcast', 'url': 'https://example.com/relationship-therapy', 'is_free': True},
            {'title': 'Sleep Stories: Guided Relaxation for Rest', 'description': 'Bedtime podcast featuring calming stories designed to help you fall asleep peacefully.', 'resource_type': 'podcast', 'url': 'https://example.com/sleep-stories', 'is_free': True},
            
            # MOBILE APPS (10)
            {'title': 'Headspace: Meditation Made Simple', 'description': 'Popular meditation and mindfulness app with guided sessions for all levels.', 'resource_type': 'app', 'url': 'https://www.headspace.com', 'is_free': False},
            {'title': 'Calm: Sleep, Meditation & Relaxation', 'description': 'Award-winning app for sleep, meditation, and relaxation with extensive content library.', 'resource_type': 'app', 'url': 'https://www.calm.com', 'is_free': False},
            {'title': 'Mood Meter: Track Your Emotional Wellbeing', 'description': 'App for tracking mood, identifying patterns, and understanding emotional triggers.', 'resource_type': 'app', 'url': 'https://example.com/mood-meter', 'is_free': True},
            {'title': 'Insight Timer: Free Meditation App', 'description': 'Free meditation app with thousands of guided meditations and music tracks.', 'resource_type': 'app', 'url': 'https://insighttimer.com', 'is_free': True},
            {'title': 'Happify: Science-Based Activities & Games', 'description': 'App using science-based activities and games to build resilience and happiness skills.', 'resource_type': 'app', 'url': 'https://www.happify.com', 'is_free': False},
            {'title': 'Sanvello: Mental Health Support On-the-Go', 'description': 'Comprehensive mental health app with mood tracking, guided journeys, and peer support.', 'resource_type': 'app', 'url': 'https://www.sanvello.com', 'is_free': False},
            {'title': 'Daylio: Mood Tracker & Micro Diary', 'description': 'Simple and intuitive mood tracking app to monitor your emotional wellbeing daily.', 'resource_type': 'app', 'url': 'https://daylio.net', 'is_free': True},
            {'title': 'Wysa: AI Mental Health Support', 'description': 'AI-powered chatbot providing emotional support and evidence-based therapy techniques.', 'resource_type': 'app', 'url': 'https://www.wysa.io', 'is_free': False},
            {'title': 'Pacifica: Stress & Anxiety Companion', 'description': 'App designed specifically for managing stress and anxiety with CBT techniques.', 'resource_type': 'app', 'url': 'https://www.thinkpacifica.com', 'is_free': False},
            {'title': 'Breathe2Relax: Breathing Exercise App', 'description': 'Free app providing guided breathing exercises to reduce stress and promote relaxation.', 'resource_type': 'app', 'url': 'https://example.com/breathe2relax', 'is_free': True},
            
            # BOOKS (10)
            {'title': 'The Anxiety and Phobia Workbook', 'description': 'Comprehensive self-help book for managing anxiety and phobias with practical exercises.', 'resource_type': 'book', 'url': 'https://example.com/anxiety-workbook', 'is_free': False},
            {'title': 'Feeling Good: The New Mood Therapy', 'description': 'Groundbreaking book on cognitive behavioral therapy for depression and anxiety.', 'resource_type': 'book', 'url': 'https://example.com/feeling-good', 'is_free': False},
            {'title': 'The Body Keeps the Score: Brain, Mind, and Body', 'description': 'Essential reading on trauma, its effects, and pathways to healing and recovery.', 'resource_type': 'book', 'url': 'https://example.com/body-keeps-score', 'is_free': False},
            {'title': 'Daring Greatly: How the Courage to Be Vulnerable', 'description': 'Book on vulnerability, courage, and building resilience in personal and professional life.', 'resource_type': 'book', 'url': 'https://example.com/daring-greatly', 'is_free': False},
            {'title': 'Wherever You Go, There You Are: Mindfulness Meditation', 'description': 'Classic guide to mindfulness meditation and its application in daily life.', 'resource_type': 'book', 'url': 'https://example.com/mindfulness-book', 'is_free': False},
            {'title': 'The Gifts of Imperfection: Let Go of Who You Think', 'description': 'Guide to wholehearted living and embracing imperfection for greater happiness.', 'resource_type': 'book', 'url': 'https://example.com/gifts-imperfection', 'is_free': False},
            {'title': 'Man\'s Search for Meaning', 'description': 'Profound exploration of finding meaning and purpose even in the most difficult circumstances.', 'resource_type': 'book', 'url': 'https://example.com/mans-search', 'is_free': False},
            {'title': 'The Mindful Way Through Depression', 'description': 'Book combining mindfulness meditation with cognitive therapy for depression relief.', 'resource_type': 'book', 'url': 'https://example.com/mindful-depression', 'is_free': False},
            {'title': 'Atomic Habits: An Easy & Proven Way', 'description': 'Guide to building good habits and breaking bad ones for lasting positive change.', 'resource_type': 'book', 'url': 'https://example.com/atomic-habits', 'is_free': False},
            {'title': 'Self-Compassion: The Proven Power of Being Kind', 'description': 'Book on developing self-compassion as a key component of mental health and wellbeing.', 'resource_type': 'book', 'url': 'https://example.com/self-compassion', 'is_free': False},
            
            # WEBSITES (10)
            {'title': 'National Institute of Mental Health (NIMH)', 'description': 'Government resource with research, statistics, and comprehensive mental health information.', 'resource_type': 'website', 'url': 'https://www.nimh.nih.gov', 'is_free': True},
            {'title': 'Mental Health America', 'description': 'Community-based nonprofit providing resources, tools, and support for mental health.', 'resource_type': 'website', 'url': 'https://www.mhanational.org', 'is_free': True},
            {'title': 'Anxiety and Depression Association of America (ADAA)', 'description': 'Resources, support groups, and information about anxiety and depression disorders.', 'resource_type': 'website', 'url': 'https://adaa.org', 'is_free': True},
            {'title': 'Psychology Today: Therapist Finder', 'description': 'Find licensed therapists and mental health professionals in your local area.', 'resource_type': 'website', 'url': 'https://www.psychologytoday.com/us/therapists', 'is_free': True},
            {'title': 'American Psychological Association Help Center', 'description': 'Evidence-based resources and information about mental health and psychological issues.', 'resource_type': 'website', 'url': 'https://www.apa.org/helpcenter', 'is_free': True},
            {'title': 'National Alliance on Mental Illness (NAMI)', 'description': 'Grassroots mental health organization providing support, education, and advocacy.', 'resource_type': 'website', 'url': 'https://www.nami.org', 'is_free': True},
            {'title': 'Mind.org.uk: Mental Health Information', 'description': 'UK-based mental health charity providing information and support for various conditions.', 'resource_type': 'website', 'url': 'https://www.mind.org.uk', 'is_free': True},
            {'title': 'The Mighty: Mental Health Community', 'description': 'Online community sharing stories, resources, and support for mental health conditions.', 'resource_type': 'website', 'url': 'https://themighty.com', 'is_free': True},
            {'title': 'Psych Central: Mental Health Resources', 'description': 'Online mental health resource with articles, quizzes, and information about conditions.', 'resource_type': 'website', 'url': 'https://psychcentral.com', 'is_free': True},
            {'title': 'Mental Health First Aid', 'description': 'Training program to help people assist someone experiencing a mental health crisis.', 'resource_type': 'website', 'url': 'https://www.mentalhealthfirstaid.org', 'is_free': False},
            
            # HELPLINES (10)
            {'title': '988 Suicide & Crisis Lifeline', 'description': '24/7 free and confidential support for people in distress, prevention and crisis resources.', 'resource_type': 'helpline', 'phone': '988', 'is_free': True},
            {'title': 'Crisis Text Line', 'description': '24/7 crisis support via text message. Text HOME to 741741 for immediate help.', 'resource_type': 'helpline', 'phone': '741741', 'is_free': True},
            {'title': 'National Domestic Violence Hotline', 'description': '24/7 support for victims and survivors of domestic violence.', 'resource_type': 'helpline', 'phone': '1-800-799-7233', 'is_free': True},
            {'title': 'SAMHSA National Helpline', 'description': 'Free, confidential, 24/7 treatment referral and information service for mental health and substance use.', 'resource_type': 'helpline', 'phone': '1-800-662-4357', 'is_free': True},
            {'title': 'National Sexual Assault Hotline', 'description': '24/7 confidential support for victims of sexual assault.', 'resource_type': 'helpline', 'phone': '1-800-656-4673', 'is_free': True},
            {'title': 'Veterans Crisis Line', 'description': '24/7 confidential support for Veterans and their families and friends.', 'resource_type': 'helpline', 'phone': '1-800-273-8255', 'is_free': True},
            {'title': 'Childhelp National Child Abuse Hotline', 'description': '24/7 professional crisis counselors for children and adults affected by child abuse.', 'resource_type': 'helpline', 'phone': '1-800-422-4453', 'is_free': True},
            {'title': 'The Trevor Project (LGBTQ+)', 'description': '24/7 crisis intervention and suicide prevention services for LGBTQ+ youth.', 'resource_type': 'helpline', 'phone': '1-866-488-7386', 'is_free': True},
            {'title': 'National Eating Disorders Association (NEDA)', 'description': 'Support, resources, and treatment options for eating disorders.', 'resource_type': 'helpline', 'phone': '1-800-931-2237', 'is_free': True},
            {'title': 'Substance Abuse and Mental Health Services Administration', 'description': '24/7 treatment referral and information service for mental health and substance use disorders.', 'resource_type': 'helpline', 'phone': '1-800-662-4357', 'is_free': True},
            
            # SUPPORT GROUPS (10)
            {'title': 'NAMI Support Groups', 'description': 'Peer-led support groups for people living with mental health conditions and their families.', 'resource_type': 'support_group', 'url': 'https://www.nami.org/Support-Education/Support-Groups', 'is_free': True},
            {'title': 'Depression and Bipolar Support Alliance (DBSA)', 'description': 'Peer support groups for people living with depression and bipolar disorder.', 'resource_type': 'support_group', 'url': 'https://www.dbsalliance.org', 'is_free': True},
            {'title': 'ADAA Online Support Groups', 'description': 'Online support groups for anxiety, depression, and related disorders.', 'resource_type': 'support_group', 'url': 'https://adaa.org/supportgroups', 'is_free': True},
            {'title': 'SMART Recovery', 'description': 'Science-based addiction recovery support groups with in-person and online meetings.', 'resource_type': 'support_group', 'url': 'https://www.smartrecovery.org', 'is_free': True},
            {'title': 'GriefShare: Grief Support Groups', 'description': 'Support groups for people dealing with the loss of a loved one.', 'resource_type': 'support_group', 'url': 'https://www.griefshare.org', 'is_free': True},
            {'title': 'Codependents Anonymous (CoDA)', 'description': 'Twelve-step program for people seeking to develop healthy relationships.', 'resource_type': 'support_group', 'url': 'https://coda.org', 'is_free': True},
            {'title': 'Mental Health Peer Support Groups', 'description': 'Local peer support groups for mental health recovery and wellness.', 'resource_type': 'support_group', 'url': 'https://example.com/peer-support', 'is_free': True},
            {'title': 'Workplace Stress Support Network', 'description': 'Online support group for people dealing with workplace stress and burnout.', 'resource_type': 'support_group', 'url': 'https://example.com/workplace-support', 'is_free': True},
            {'title': 'Trauma Survivors Support Group', 'description': 'Safe space for trauma survivors to share experiences and find support.', 'resource_type': 'support_group', 'url': 'https://example.com/trauma-support', 'is_free': True},
            {'title': 'LGBTQ+ Mental Health Support Groups', 'description': 'Support groups specifically for LGBTQ+ individuals facing mental health challenges.', 'resource_type': 'support_group', 'url': 'https://example.com/lgbtq-support', 'is_free': True},
            
            # THERAPY SERVICES (10)
            {'title': 'BetterHelp Online Therapy', 'description': 'Online therapy platform connecting you with licensed therapists via video, phone, or chat.', 'resource_type': 'therapy', 'url': 'https://www.betterhelp.com', 'is_free': False},
            {'title': 'Talkspace Online Therapy', 'description': 'Online therapy and psychiatry services with flexible communication options.', 'resource_type': 'therapy', 'url': 'https://www.talkspace.com', 'is_free': False},
            {'title': 'Amwell: Therapy and Psychiatry', 'description': 'Virtual therapy and psychiatry services with board-certified professionals.', 'resource_type': 'therapy', 'url': 'https://www.amwell.com', 'is_free': False},
            {'title': 'Open Path Psychotherapy Collective', 'description': 'Affordable therapy services connecting clients with therapists offering reduced rates.', 'resource_type': 'therapy', 'url': 'https://openpathcollective.org', 'is_free': False},
            {'title': 'Psychology Today: Find a Therapist', 'description': 'Comprehensive directory to find licensed therapists and counselors in your area.', 'resource_type': 'therapy', 'url': 'https://www.psychologytoday.com', 'is_free': True},
            {'title': 'Cerebral: Online Mental Health Care', 'description': 'Online therapy and medication management for anxiety, depression, and more.', 'resource_type': 'therapy', 'url': 'https://cerebral.com', 'is_free': False},
            {'title': 'Brightside: Online Depression & Anxiety Treatment', 'description': 'Online therapy and medication treatment for depression and anxiety disorders.', 'resource_type': 'therapy', 'url': 'https://www.brightside.com', 'is_free': False},
            {'title': 'Sondermind: Personalized Therapy', 'description': 'Matching service connecting you with therapists who specialize in your specific needs.', 'resource_type': 'therapy', 'url': 'https://www.sondermind.com', 'is_free': False},
            {'title': 'Ginger: On-Demand Mental Health Support', 'description': '24/7 access to behavioral health coaches, therapists, and psychiatrists.', 'resource_type': 'therapy', 'url': 'https://www.ginger.com', 'is_free': False},
            {'title': 'Lyra Health: Workplace Mental Health Benefits', 'description': 'Employer-sponsored mental health benefits providing access to quality therapy.', 'resource_type': 'therapy', 'url': 'https://www.lyrahealth.com', 'is_free': False},
            
            # OTHER (10)
            {'title': 'Mental Health First Aid Training', 'description': 'Training program teaching skills to help someone experiencing a mental health crisis.', 'resource_type': 'other', 'url': 'https://www.mentalhealthfirstaid.org', 'is_free': False},
            {'title': 'Crisis Intervention Training', 'description': 'Professional training in crisis intervention techniques for mental health situations.', 'resource_type': 'other', 'url': 'https://example.com/crisis-training', 'is_free': False},
            {'title': 'Mental Health Assessment Tools', 'description': 'Online screening tools and assessments for various mental health conditions.', 'resource_type': 'other', 'url': 'https://example.com/assessments', 'is_free': True},
            {'title': 'Workplace Wellness Programs', 'description': 'Resources for implementing mental health and wellness programs in the workplace.', 'resource_type': 'other', 'url': 'https://example.com/workplace-wellness', 'is_free': False},
            {'title': 'Peer Support Training Program', 'description': 'Training program for becoming a certified peer support specialist.', 'resource_type': 'other', 'url': 'https://example.com/peer-training', 'is_free': False},
            {'title': 'Mental Health Awareness Campaigns', 'description': 'Resources and materials for raising mental health awareness in your community.', 'resource_type': 'other', 'url': 'https://example.com/awareness', 'is_free': True},
            {'title': 'Wellness Coaching Services', 'description': 'Holistic wellness coaching combining mental health support with lifestyle guidance.', 'resource_type': 'other', 'url': 'https://example.com/wellness-coaching', 'is_free': False},
            {'title': 'Mental Health Research Database', 'description': 'Access to research papers and studies on mental health and treatment outcomes.', 'resource_type': 'other', 'url': 'https://example.com/research', 'is_free': True},
            {'title': 'Crisis Response Training for First Responders', 'description': 'Specialized training for police, fire, and EMS on mental health crisis response.', 'resource_type': 'other', 'url': 'https://example.com/first-responder-training', 'is_free': False},
            {'title': 'Mental Health Advocacy Resources', 'description': 'Tools and resources for advocating for mental health policy and access to care.', 'resource_type': 'other', 'url': 'https://example.com/advocacy', 'is_free': True},
        ]
        
        # Get categories for resource assignment
        crisis_category = ResourceCategory.objects.filter(name='Crisis Support').first()
        self_care_category = ResourceCategory.objects.filter(name='Self-Care').first()
        professional_category = ResourceCategory.objects.filter(name='Professional Help').first()
        education_category = ResourceCategory.objects.filter(name='Education').first()
        default_category = ResourceCategory.objects.first()
        
        resources_created = 0
        for res_data in resources_data:
            # Assign category based on resource type
            if res_data['resource_type'] == 'helpline':
                category = crisis_category or default_category
            elif res_data['resource_type'] in ['app', 'book']:
                category = self_care_category or default_category
            elif res_data['resource_type'] in ['therapy', 'support_group']:
                category = professional_category or default_category
            else:
                category = education_category or default_category
            
            res_data['category'] = category
            res_data['is_verified'] = True
            res_data['is_active'] = True
            
            resource, created = Resource.objects.get_or_create(
                title=res_data['title'],
                defaults=res_data
            )
            if created:
                resources_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {resources_created} resources (10 for each of the 10 resource types)'))
        
        # Create guidance content
        guidance_data = [
            {
                'risk_level': 'low',
                'title': 'Maintaining Your Mental Wellness',
                'content': 'You\'re doing great! Here are some tips to maintain your mental health.',
                'self_care_tips': 'Continue regular exercise, maintain social connections, practice mindfulness.',
                'when_to_seek_help': 'If you notice any changes in your mood or behavior.',
                'emergency_resources': 'Keep crisis numbers handy: 988 for Suicide & Crisis Lifeline.'
            },
            {
                'risk_level': 'moderate',
                'title': 'Building Resilience and Seeking Support',
                'content': 'There are some areas where additional support could be helpful.',
                'self_care_tips': 'Practice stress management, maintain sleep hygiene, engage in enjoyable activities.',
                'when_to_seek_help': 'Consider speaking with a mental health professional if symptoms persist.',
                'emergency_resources': '988 Suicide & Crisis Lifeline, Crisis Text Line: Text HOME to 741741'
            },
            {
                'risk_level': 'high',
                'title': 'Immediate Support and Professional Help',
                'content': 'Professional support is recommended to help you through this time.',
                'self_care_tips': 'Prioritize safety, reach out to trusted individuals, avoid isolation.',
                'when_to_seek_help': 'Contact a mental health professional immediately or go to the nearest emergency room.',
                'emergency_resources': '988 Suicide & Crisis Lifeline, 911 for emergencies, Crisis Text Line: Text HOME to 741741'
            }
        ]
        
        for guidance in guidance_data:
            GuidanceContent.objects.get_or_create(
                risk_level=guidance['risk_level'],
                defaults=guidance
            )
        
        # Create crisis resources
        crisis_data = [
            {
                'name': '988 Suicide & Crisis Lifeline',
                'description': '24/7 crisis support and suicide prevention',
                'phone': '988',
                'is_24_7': True,
                'priority': 1
            },
            {
                'name': 'Crisis Text Line',
                'description': '24/7 crisis support via text',
                'phone': '741741',
                'is_24_7': True,
                'priority': 2
            },
            {
                'name': 'National Alliance on Mental Illness (NAMI)',
                'description': 'Mental health support and resources',
                'phone': '1-800-950-NAMI',
                'website': 'https://www.nami.org',
                'is_24_7': False,
                'priority': 3
            }
        ]
        
        for crisis in crisis_data:
            CrisisResource.objects.get_or_create(
                name=crisis['name'],
                defaults=crisis
            )
        
        # Create FAQ
        faq_data = [
            {
                'question': 'Is this assessment a substitute for professional medical advice?',
                'answer': 'No, this assessment is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.',
                'category': 'General',
                'order': 1
            },
            {
                'question': 'How often should I take the assessment?',
                'answer': 'You can take the assessment as often as you like. We recommend monthly check-ins to track your progress.',
                'category': 'Assessment',
                'order': 2
            },
            {
                'question': 'Is my data secure and private?',
                'answer': 'Yes, we take your privacy seriously. All data is encrypted and stored securely. We never share your personal information.',
                'category': 'Privacy',
                'order': 3
            },
            {
                'question': 'What should I do if I\'m in crisis?',
                'answer': 'If you\'re experiencing a mental health crisis, please contact 988 (Suicide & Crisis Lifeline) or go to your nearest emergency room.',
                'category': 'Crisis',
                'order': 4
            }
        ]
        
        for faq in faq_data:
            FAQ.objects.get_or_create(
                question=faq['question'],
                defaults=faq
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )

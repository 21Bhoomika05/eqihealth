from app.models import db, Resource

def populate_resources():
    # Example resources
    resources = [
        Resource(title='Health Equity: A Critical Perspective', url='https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5838795/'),
        Resource(title='Health Equity and Social Justice', url='https://www.who.int/news-room/fact-sheets/detail/social-determinants-of-health'),
        Resource(title='The Role of Health Equity in Public Health', url='https://www.cdc.gov/healthequity/index.html'),
        Resource(title='Understanding Health Equity', url='https://www.rwjf.org/en/library/research/2020/01/understanding-health-equity.html'),
        Resource(title='COVID-19 and Health Equity: A Global Perspective', url='https://www.who.int/news-room/feature-stories/detail/covid-19-and-health-equity'),
        Resource(title='Public Health Resources and Research', url='https://www.apha.org/Research-and-Publications'),
        Resource(title='Health Disparities: A Persistent Problem', url='https://www.ama-assn.org/delivering-care/public-health/health-disparities-persistent-problem'),
        Resource(title='Papers and Articles on Health Equity', url='https://www.healthaffairs.org/do/10.1377/hblog20200803.983847/full/'),
        Resource(title='Health Equity in America', url='https://www.healthypeople.gov/2020/topics-objectives/topic/social-determinants-of-health'),
        Resource(title='Understanding Racial and Ethnic Disparities', url='https://www.ahrq.gov/research/findings/final-reports/healthdisparities/index.html'),
        Resource(title='WHO: Health Equity', url='https://www.who.int/health-topics/health-equity'),
        Resource(title='National Institute for Health Equity', url='https://www.nhlbi.nih.gov/about/org/health-equity'),
        Resource(title='Health Equity: The Role of Social Determinants', url='https://www.urban.org/research/publication/health-equity-role-social-determinants/view/full_report'),
        Resource(title='Equity in Health Care: An International Perspective', url='https://www.healthaffairs.org/doi/full/10.1377/hlthaff.2020.00620'),
        Resource(title='Guide to Health Equity Resources', url='https://www.cdc.gov/nccdphp/dch/programs/health-equity/guide.htm')
    ]

    db.create_all()  # Create tables if they don't exist
    db.session.bulk_save_objects(resources)
    db.session.commit()

if __name__ == '__main__':
    populate_resources()

import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const Home = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-white text-center px-4">
      <div className="flex items-center justify-center py-4 px-10">
        <h2 className="text-2xl mb-2 font-semibold text-[#a5a0bc]">
          {t('definitionHeading')}
        </h2>
      </div>

      <h1 className="text-7xl font-bold mb-6 leading-[1.15] bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] text-transparent bg-clip-text">
        {t('mainTitle')}
      </h1>

      <p className="text-lg mb-6 max-w-4xl text-white">
        {t('description')}
      </p>

      <div className="flex space-x-4 mt-2 mb-6">
        <div className="p-[2px] rounded-full bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] inline-block hover:opacity-90 transition">
          <button
            className="bg-[#0F0A27] text-white font-semibold py-3 px-14 rounded-full"
            onClick={() => navigate('/vibeprogramminglanguage/docs')}
          >
            {t('learnMore')}
          </button>
        </div>
        <button
          className="bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] text-white font-semibold py-3 px-14 rounded-full hover:opacity-90 transition"
          onClick={() => navigate('/vibeprogramminglanguage/playground')}
        >
          {t('codeNow')}
        </button>
      </div>

      <div className="relative w-full max-w-5xl py-12 px-4 rounded-lg text-white overflow-hidden mt-6 mb-12">
        <div
          className="absolute inset-0 bg-cover bg-center opacity-10"
          style={{ backgroundImage: "url('/Container.svg')" }}
          aria-hidden="true"
        />
        <div className="relative z-10 flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-12 text-left">
          <div className="flex items-center space-x-3">
            <span className="text-4xl text-[#924DC2] font-bold">{t('stat1.value')}</span>
            <div className="leading-tight text-sm">
              <div>{t('stat1.line1')}</div>
              <div>{t('stat1.line2')}</div>
            </div>
          </div>
          <div className="hidden md:block w-0.5 h-10 bg-[#817D92]"></div>
          <div className="flex items-center space-x-3">
            <span className="text-4xl text-[#924DC2] font-bold">{t('stat2.value')}</span>
            <div className="leading-tight text-sm">
              <div>{t('stat2.line1')}</div>
              <div>{t('stat2.line2')}</div>
            </div>
          </div>
          <div className="hidden md:block w-0.5 h-10 bg-[#817D92]"></div>
          <div className="flex items-center space-x-3">
            <span className="text-4xl text-[#924DC2] font-bold">{t('stat3.value')}</span>
            <div className="leading-tight text-sm">
              <div>{t('stat3.line1')}</div>
              <div>{t('stat3.line2')}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

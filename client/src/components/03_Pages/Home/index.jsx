import Hero from '@/components/04_Widgets/Content/Display/hero';
import ServSection from '@/components/04_Widgets/Content/Display/servSection';
import Footer from '@/components/04_Widgets/Navigation/Menus/footer';
import usePageTitle from '@/hooks/usePageTitle';

const HomePage = () => {
  usePageTitle('home');

  return (
    <>
      <Hero />
      <ServSection />
      <Footer />
    </>
  );
};

export default HomePage;

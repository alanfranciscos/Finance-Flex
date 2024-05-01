'use client';

import InformationsContainer from './components/InformationsContainer';
import { MainContainer } from './styles';
import InputsContainer from './components/InputsContainer';

export default function HomePage() {
  return (
    <MainContainer>
      <InformationsContainer />
      <InputsContainer />
    </MainContainer>
  );
}

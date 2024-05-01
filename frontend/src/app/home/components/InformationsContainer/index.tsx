'use client';
import { Container, Content, ChartImage, ContentText, Title } from './styles';

export default function InformationsContainer() {
  return (
    <Container>
      <Title>Finance Flex</Title>
      <Content>
        <ContentText>
          Bem-vindo ao Finance Flex, sua solução completa para o gerenciamento
          financeiro pessoal. Este aplicativo foi desenvolvido para proporcionar
          uma experiência intuitiva e eficaz no planejamento financeiro,
          permitindo que você assuma o controle total das suas finanças de
          maneira inteligente e simplificada.
        </ContentText>
        <ChartImage src="/images/chart.svg" alt="chart" />
      </Content>
    </Container>
  );
}

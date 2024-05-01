'use client';

import {
  Container,
  InputContainer,
  LoginContainer,
  LogoImage,
  NewAccountAnchor,
  NewAccountContainer,
  NewAccountText,
} from './styles';

import Input from '@components/Input';
import Button from '@components/Button';

import { useRouter } from 'next/navigation';

export default function InputsContainer() {
  const router = useRouter();

  return (
    <Container>
      <LoginContainer>
        <LogoImage src="/images/logo.svg" alt="Logo" />
        <InputContainer>
          <Input
            title="E-mail"
            type="email"
            placeholder="Digite seu e-mail"
            value=""
          />
          <Input
            title="Senha"
            type="password"
            placeholder="Digite seu e-mail"
            value=""
            footerText="Esqueci a senha"
          />
        </InputContainer>
        <Button text="Entrar" onClick={() => null} />
      </LoginContainer>
      <NewAccountContainer>
        <NewAccountText>
          Ainda não possui uma conta?
          <NewAccountAnchor onClick={() => router.push('/create-account')}>
            Cadastre-se
          </NewAccountAnchor>
        </NewAccountText>
      </NewAccountContainer>
    </Container>
  );
}

import styled from 'styled-components';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
`;

export const LoginContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;

  width: 25rem;
  border-radius: 0.625rem;
  border: 1px solid var(--Gray-01, #a9a9a9);

  padding: 2.25rem;
`;

export const LogoImage = styled.img`
  width: 9.375rem;
  height: 9.375rem;

  margin-bottom: 3rem;
`;

export const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 1.25rem;
  margin-bottom: 3rem;
`;

export const NewAccountContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;

  border-radius: 0.625rem;
  border: 1px solid var(--Gray-01, #a9a9a9);

  padding: 0.5rem;
`;

export const NewAccountText = styled.p``;

export const NewAccountAnchor = styled.a`
  cursor: pointer;
  color: var(--green, #2de08d);
  margin-left: 0.3125rem;
`;

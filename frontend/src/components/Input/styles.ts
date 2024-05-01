import styled from 'styled-components';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  width: 25rem;
`;

export const InputTitle = styled.span``;

export const InputContent = styled.input`
  height: 2.125rem;
  border-radius: 0.3125rem;
  border: 1px solid var(--Gray-01, #a9a9a9);
  padding-left: 0.5rem;
`;

export const InputFooter = styled.p`
  margin-top: 0.1125rem;
  text-align: right;
`;

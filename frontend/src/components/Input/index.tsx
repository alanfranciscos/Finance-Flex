import { Container, InputContent, InputFooter, InputTitle } from './styles';
import InputProps from './types';

export default function Input({
  title,
  type,
  placeholder,
  value,
  footerText,
  onChange,
}: InputProps) {
  return (
    <Container>
      <InputTitle>{title}</InputTitle>
      <InputContent
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
      {footerText && <InputFooter>{footerText}</InputFooter>}
    </Container>
  );
}

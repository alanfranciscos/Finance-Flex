import { ButtonStyle } from './styles';
import ButtonProps from './types';

export default function Button({ text, onClick }: ButtonProps) {
  return <ButtonStyle onClick={() => onClick}>{text}</ButtonStyle>;
}

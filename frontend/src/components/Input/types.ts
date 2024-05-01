export default interface InputProps {
  title?: string;
  type: string;
  placeholder: string;
  value: string;
  footerText?: string;
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

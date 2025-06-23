@Entity()
export class Document {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  content: string;

  @Column()
  uploadDate: Date;
}
